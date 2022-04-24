<template>
  <div class="main-container" style="overflow: auto;">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/projects/projectList' }">项目列表</el-breadcrumb-item>
        <el-breadcrumb-item :to="{
          path: '/projects/projectHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.$route.query.projectName
          }
        }">{{this.$route.query.projectName}}</el-breadcrumb-item>
        <el-breadcrumb-item :to="{
          path: '/projects/projectProfile',
          query: {
            projectId: this.$route.query.projectId
          }
        }">项目信息</el-breadcrumb-item>
        <el-breadcrumb-item>基线管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <el-row :gutter="20">
        <!-- 需求条目树区 -->
        <el-col :span="6">
          <el-tree :data="requirementTree" @node-click="handleNodeClick" style="overflow: auto;"
          node-key="_id" highlight-current :current-node-key="currentNodeKey"
          :expand-on-click-node="false" :default-expanded-keys="defaultExpandedKey"
          :render-content="renderTreeContent">
          </el-tree>
        </el-col>
        <!-- 需求表格区 -->
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
  created () {
    // 获取上一页传递过来的Id和Name
    this.projectId = this.$route.query.projectId
    this.projectName = this.$route.query.projectName
    this.currentNodeKey = this.$route.query.requirementId
    if (this.currentNodeKey) {
      this.defaultExpandedKey.push(this.currentNodeKey)
    }
    // 获取需求树
    this.getRequirementTree()
  },
  data () {
    return {
      projectId: '',
      projectName: '',
      currentNodeKey: '',
      defaultExpandedKey: [],
      requirementTree: [
        {
          _id: '2',
          label: '1 功能需求',
          children: []
        },
        {
          _id: '3',
          label: '2 性能需求',
          children: []
        },
        {
          _id: '4',
          label: '3 可靠性需求',
          children: []
        },
        {
          _id: '7',
          label: '4 安全性需求',
          children: []
        }
      ]
    }
  },
  methods: {
    async getRequirementTree () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/requirement/archive/tree/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: this.projectId,
          version: this.$route.query.version
        }
      })
      if (res.meta.status === 200) {
        this.requirementTree = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 给需求树增添样式
    renderTreeContent (h, { node, data, store }) {
      if (['2', '3', '4', '7'].includes(node.data._id)) {
        return (<span style="font-size: 15px; font-weight: bold;">{node.label}</span>)
      } else return (<span style="font-size: 14px;">{node.label}</span>)
    },
    handleNodeClick (data) {
      this.currentNodeKey = data._id
      this.jumpRequirementHomepage(data._id)
    },
    jumpRequirementHomepage (requirementId) {
      // 点击需求标签不跳转
      if (['2', '3', '4', '7'].includes(requirementId)) return

      this.$router.push({
        path: '/requirements/archive/requirementHomepage',
        query: {
          projectId: this.projectId,
          projectName: this.projectName,
          requirementId: requirementId,
          version: this.$route.query.version
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.main-container {
  height: 100%;
}
</style>
