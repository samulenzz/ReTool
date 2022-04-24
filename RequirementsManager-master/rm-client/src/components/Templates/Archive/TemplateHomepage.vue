<template>
  <div class="main-container" style="overflow: auto">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模板管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/templates/templateList' }">
          模板列表
        </el-breadcrumb-item>
        <el-breadcrumb-item
          :to="{
            path: '/templates/templateHomepage',
            query: {
              templateId: this.$route.query.templateId,
              templateName: this.$route.query.templateName,
            },
          }"
          >{{ this.$route.query.templateName }}</el-breadcrumb-item
        >
        <el-breadcrumb-item
          :to="{
            path: '/templates/templateProfile',
            query: {
              templateId: this.$route.query.templateId,
            },
          }"
          >模板信息</el-breadcrumb-item
        >
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <el-row :gutter="20">
        <!-- 条目树区 -->
        <el-col :span="6">
          <el-tree
            :data="requirementTree"
            @node-click="handleNodeClick"
            style="overflow: auto"
            node-key="_id"
            highlight-current
            :current-node-key="currentNodeKey"
            :expand-on-click-node="false"
            :default-expanded-keys="defaultExpandedKey"
            :render-content="renderTreeContent"
          >
          </el-tree>
        </el-col>
        <!-- 表格区 -->
        <el-col :span="18">
          <!-- 加key是为了刷新子页面 -->
          <!-- https://segmentfault.com/q/1010000015992883 -->
          <router-view :key="$route.fullPath"></router-view>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  created() {

  },
  data() {

  },
  methods: {
    
  },
};
</script>

<style lang="less" scoped>
.main-container {
  height: 100%;
}
</style>
