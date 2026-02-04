<template>
  <div class="config-page">
    <div class="page-header">
      <h2>系统配置</h2>
    </div>

    <div class="config-content">
      <EmbyConfigCard />

      <el-form :model="config" label-width="120px" class="config-form">
        <el-divider>夸克网盘配置（待完善）</el-divider>

        <el-form-item label="Cookie">
          <el-input
            v-model="config.cookie"
            type="textarea"
            :rows="3"
            placeholder="请输入夸克网盘Cookie"
            show-password
          />
        </el-form-item>

        <el-form-item label="根目录ID">
          <el-input v-model="config.rootId" placeholder="0" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="saveConfig">保存（待实现）</el-button>
          <el-button @click="resetConfig">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import EmbyConfigCard from '@/components/EmbyConfigCard.vue'

const config = reactive({
  cookie: '',
  rootId: '0'
})

const saveConfig = () => {
  ElMessage.info('该区域配置保存功能待实现')
}

const resetConfig = () => {
  ElMessage.info('配置已重置')
}
</script>

<style scoped>
.config-page {
  padding: 8px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.config-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  max-width: 800px;
}

.config-form {
  margin-top: 20px;
}
</style>
