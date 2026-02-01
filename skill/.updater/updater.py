#!/usr/bin/env python3
"""
Skill 自动更新系统

根据开源项目更新自动维护 Skill 内容。
支持定时任务和手动触发两种方式。
"""

import os
import sys
import yaml
import json
import logging
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('skill-updater')


class UpdateType(Enum):
    """更新类型"""
    BREAKING_CHANGE = "breaking_change"
    NEW_FEATURE = "new_feature"
    BUG_FIX = "bug_fix"
    DOCS_UPDATE = "docs_update"
    BEST_PRACTICE = "best_practice"


class VersionBump(Enum):
    """版本升级类型"""
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclass
class SkillInfo:
    """Skill 信息"""
    name: str
    path: str
    version: str
    scope: str
    content: str


@dataclass
class ProjectRelease:
    """项目发布信息"""
    project_name: str
    version: str
    release_notes: str
    published_at: datetime
    html_url: str


@dataclass
class UpdatePlan:
    """更新计划"""
    skill_name: str
    skill_path: str
    current_version: str
    new_version: str
    changes: List[Dict]
    update_type: UpdateType
    reason: str


class SkillUpdater:
    """Skill 更新器"""
    
    def __init__(self, config_path: str = ".updater/config.yaml"):
        """初始化更新器"""
        self.config = self._load_config(config_path)
        self.cache_dir = Path(self.config['cache']['directory'])
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # GitHub API Token
        self.github_token = os.getenv('GITHUB_TOKEN', '')
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            sys.exit(1)
    
    def _get_github_headers(self) -> Dict[str, str]:
        """获取 GitHub API 请求头"""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Skill-Updater/1.0'
        }
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        return headers
    
    def _get_cached_data(self, cache_key: str, ttl: int) -> Optional[Dict]:
        """获取缓存数据"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        
        # 检查缓存是否过期
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime > timedelta(seconds=ttl):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
            return None
    
    def _set_cached_data(self, cache_key: str, data: Dict):
        """设置缓存数据"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"写入缓存失败: {e}")
    
    def fetch_project_releases(self, repo: str) -> List[ProjectRelease]:
        """获取项目发布信息"""
        cache_key = hashlib.md5(f"releases_{repo}".encode()).hexdigest()
        ttl = self.config['cache']['release_info_ttl']
        
        # 尝试从缓存获取
        cached = self._get_cached_data(cache_key, ttl)
        if cached:
            logger.info(f"使用缓存的 releases: {repo}")
            return [ProjectRelease(**r) for r in cached]
        
        # 从 GitHub API 获取
        url = f"https://api.github.com/repos/{repo}/releases"
        headers = self._get_github_headers()
        
        try:
            response = requests.get(
                url, 
                headers=headers,
                timeout=self.config['security']['request_timeout']
            )
            response.raise_for_status()
            
            releases_data = response.json()
            releases = []
            
            for release in releases_data[:5]:  # 只取最近 5 个
                releases.append(ProjectRelease(
                    project_name=repo.split('/')[-1],
                    version=release['tag_name'],
                    release_notes=release.get('body', ''),
                    published_at=datetime.fromisoformat(
                        release['published_at'].replace('Z', '+00:00')
                    ),
                    html_url=release['html_url']
                ))
            
            # 缓存数据
            self._set_cached_data(cache_key, [asdict(r) for r in releases])
            
            return releases
            
        except requests.RequestException as e:
            logger.error(f"获取 releases 失败: {e}")
            return []
    
    def load_skill(self, skill_path: str) -> Optional[SkillInfo]:
        """加载 Skill 信息"""
        skill_file = Path(skill_path) / "SKILL.md"
        if not skill_file.exists():
            logger.warning(f"Skill 文件不存在: {skill_file}")
            return None
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 frontmatter
            if content.startswith('---'):
                _, frontmatter, body = content.split('---', 2)
                metadata = yaml.safe_load(frontmatter)
            else:
                metadata = {}
                body = content
            
            return SkillInfo(
                name=metadata.get('name', ''),
                path=skill_path,
                version=metadata.get('version', '1.0.0'),
                scope=metadata.get('scope', ''),
                content=content
            )
            
        except Exception as e:
            logger.error(f"加载 Skill 失败: {e}")
            return None
    
    def analyze_update_impact(
        self, 
        release: ProjectRelease, 
        skill: SkillInfo
    ) -> Tuple[UpdateType, str]:
        """分析更新影响"""
        notes = release.release_notes.lower()
        
        # 判断更新类型
        if any(keyword in notes for keyword in ['breaking', 'deprecated', 'removed']):
            return UpdateType.BREAKING_CHANGE, "检测到破坏性变更"
        
        if any(keyword in notes for keyword in ['new feature', 'added', 'support']):
            return UpdateType.NEW_FEATURE, "检测到新功能"
        
        if any(keyword in notes for keyword in ['fix', 'bug', 'patch']):
            return UpdateType.BUG_FIX, "检测到 Bug 修复"
        
        if any(keyword in notes for keyword in ['docs', 'documentation']):
            return UpdateType.DOCS_UPDATE, "检测到文档更新"
        
        return UpdateType.BEST_PRACTICE, "检测到最佳实践更新"
    
    def bump_version(self, current_version: str, update_type: UpdateType) -> str:
        """升级版本号"""
        parts = current_version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        bump_type = self.config['version_bump']['mapping'].get(
            update_type.value, 'patch'
        )
        
        if bump_type == 'major':
            return f"{major + 1}.0.0"
        elif bump_type == 'minor':
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    
    def generate_update_plan(
        self, 
        skill: SkillInfo, 
        release: ProjectRelease,
        update_type: UpdateType
    ) -> UpdatePlan:
        """生成更新计划"""
        new_version = self.bump_version(skill.version, update_type)
        
        changes = []
        
        # 根据更新类型决定更新哪些 section
        if update_type == UpdateType.NEW_FEATURE:
            changes.append({
                'section': 'capabilities',
                'action': 'review',
                'reason': f"检查是否需要添加新能力（参考 {release.version}）"
            })
        
        if update_type in [UpdateType.NEW_FEATURE, UpdateType.BUG_FIX]:
            changes.append({
                'section': 'references',
                'action': 'update',
                'content': f"version: '{release.version}'",
                'reason': f"更新版本引用至 {release.version}"
            })
        
        if update_type in [UpdateType.NEW_FEATURE, UpdateType.BEST_PRACTICE]:
            changes.append({
                'section': 'examples',
                'action': 'review',
                'reason': "检查是否需要添加新示例"
            })
        
        return UpdatePlan(
            skill_name=skill.name,
            skill_path=skill.path,
            current_version=skill.version,
            new_version=new_version,
            changes=changes,
            update_type=update_type,
            reason=f"{release.project_name} 发布 {release.version}"
        )
    
    def check_updates(self) -> List[UpdatePlan]:
        """检查所有更新"""
        update_plans = []
        
        for project in self.config['tracked_projects']:
            if not project.get('track_releases', False):
                continue
            
            logger.info(f"检查项目: {project['name']}")
            
            # 获取项目发布信息
            releases = self.fetch_project_releases(project['repo'])
            
            if not releases:
                continue
            
            latest_release = releases[0]
            
            # 检查受影响的 Skill
            for skill_path in project.get('affected_skills', []):
                skill = self.load_skill(f"skill/{skill_path}")
                
                if not skill:
                    continue
                
                # 检查是否需要更新
                # 这里简化处理，实际应该比较版本号
                update_type, reason = self.analyze_update_impact(
                    latest_release, skill
                )
                
                plan = self.generate_update_plan(
                    skill, latest_release, update_type
                )
                
                update_plans.append(plan)
                logger.info(f"发现更新: {skill.name} -> {plan.new_version}")
        
        return update_plans
    
    def apply_update(self, plan: UpdatePlan) -> bool:
        """应用更新"""
        skill_file = Path(plan.skill_path) / "SKILL.md"
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新版本号
            content = content.replace(
                f'version: {plan.current_version}',
                f'version: {plan.new_version}'
            )
            
            # 这里可以添加更多更新逻辑
            # 例如更新特定 section 的内容
            
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"已更新: {plan.skill_name} ({plan.current_version} -> {plan.new_version})")
            return True
            
        except Exception as e:
            logger.error(f"应用更新失败: {e}")
            return False
    
    def create_skill_zips_in_all(self):
        """在all目录下为每个技能创建压缩包（只保留压缩包）"""
        logger.info("开始为每个技能创建压缩包到all目录...")
        
        import zipfile
        import shutil
        import os
        
        # 获取skill目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        all_dir = os.path.join(skill_dir, 'all')
        
        # 清理并重建all目录
        if os.path.exists(all_dir):
            shutil.rmtree(all_dir)
        os.makedirs(all_dir, exist_ok=True)
        
        # 获取所有技能类别目录
        skill_count = 0
        try:
            categories = [d for d in os.listdir(skill_dir) 
                         if os.path.isdir(os.path.join(skill_dir, d)) 
                         and d not in ['all', '.updater']]
            
            for category in categories:
                category_path = os.path.join(skill_dir, category)
                
                # 遍历类别下的所有技能目录
                for skill_name in os.listdir(category_path):
                    skill_path = os.path.join(category_path, skill_name)
                    skill_md_path = os.path.join(skill_path, 'SKILL.md')
                    
                    # 检查是否是技能目录且包含SKILL.md
                    if os.path.isdir(skill_path) and os.path.exists(skill_md_path):
                        # 创建技能压缩包路径
                        zip_path = os.path.join(all_dir, f"{skill_name}.zip")
                        
                        try:
                            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                                # 直接将SKILL.md添加到压缩包根目录
                                zf.write(skill_md_path, 'SKILL.md')
                                logger.info(f"已创建技能压缩包: {skill_name}.zip")
                                skill_count += 1
                        except Exception as e:
                            logger.error(f"创建 {skill_name}.zip 失败: {e}")
                            continue
            
            logger.info(f"所有技能压缩包创建完成，共 {skill_count} 个")
            return True
        except Exception as e:
            logger.error(f"创建技能压缩包失败: {e}")
            return False

    def run(self, dry_run: bool = False):
        """运行更新流程"""
        logger.info("开始检查 Skill 更新...")
        
        # 检查更新
        update_plans = self.check_updates()
        
        if not update_plans:
            logger.info("没有需要更新的 Skill")
        else:
            logger.info(f"发现 {len(update_plans)} 个需要更新的 Skill")
            
            # 应用更新
            for plan in update_plans:
                if dry_run:
                    logger.info(f"[Dry Run] 将更新: {plan.skill_name} -> {plan.new_version}")
                else:
                    self.apply_update(plan)
        
        # 创建技能压缩包到all目录（只保留压缩包）
        if not dry_run:
            self.create_skill_zips_in_all()
        
        logger.info("更新检查完成")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Skill 自动更新系统')
    parser.add_argument(
        '--config', 
        default='.updater/config.yaml',
        help='配置文件路径'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='试运行，不实际应用更新'
    )
    parser.add_argument(
        '--skill',
        help='只更新指定的 Skill'
    )
    
    args = parser.parse_args()
    
    updater = SkillUpdater(args.config)
    updater.run(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
