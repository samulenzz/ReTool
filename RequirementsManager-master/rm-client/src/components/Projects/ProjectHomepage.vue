<template>
  <div class="main-container" style="overflow: auto;">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/projects/projectList' }">项目列表</el-breadcrumb-item>
        <el-breadcrumb-item>{{projectName}}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 工具栏区 -->
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="6">
          <div><span style="color: ghostwhite;">目录</span></div>
        </el-col>
        <el-col :span="18">
          <!-- 添加需求按钮 -->
          <el-dropdown trigger="click" size="medium" @command="handleAddRequirement">
            <el-button type="primary" icon="el-icon-plus" plain round>添加</el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="addBefore">在上方插入</el-dropdown-item>
              <el-dropdown-item command="addAfter">在下方插入</el-dropdown-item>
              <el-dropdown-item command="addInner">添加子需求</el-dropdown-item>
              <el-dropdown-item command="importFile" divided>从文本导入</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <!--- 移动按钮 -->
          <el-button type="warning" icon="el-icon-sort" plain round
          @click="handleMoveRequirement()" style="margin-left: 10px;">移动</el-button>
          <!--- 删除按钮 -->
          <el-button type="danger" icon="el-icon-sort" plain round
          @click="deleteRequirement()">删除</el-button>
        </el-col>
      </el-row>
      <!-- 工具栏下部 -->
      <el-row :gutter="20">
        <!-- 需求条目树区 -->
        <el-col :span="6">
          <el-tree :data="requirementTree" @node-click="handleNodeClick" style="overflow: auto;"
          node-key="_id" highlight-current ref="requirementTreeRef"
          :expand-on-click-node="false" :default-expanded-keys="defaultExpandedKey"
          :render-content="renderTreeContent">
          </el-tree>
        </el-col>
        <!-- 需求表格区 -->
        <el-col :span="18">
          <!-- 加key是为了刷新子页面 -->
          <!-- https://segmentfault.com/q/1010000015992883 -->
          <!-- https://blog.csdn.net/u010176097/article/details/81252417 -->
          <router-view :key="$route.fullPath" @fresh="fresh"></router-view>
        </el-col>
      </el-row>
    </el-card>

    <!-- Dialog区 -->
    <!-- 移动需求条目Dialog -->
    <el-dialog title="请拖拽移动需求（只能移动当前选中需求）" :visible.sync="dialogVisible.moveRequirement" width="40%">
      <el-tree :data="moveRequirementTree" style="overflow: auto;"
      node-key="_id" highlight-current ref="moveRequirementTreeRef"
      :expand-on-click-node="false" :default-expanded-keys="moveDefaultExpandedKey"
      draggable :allow-drag="allowDrag" :allow-drop="allowDrop"
      @node-drop="handleNodeDrop" :render-content="renderTreeContent">
      </el-tree>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible.moveRequirement = false">取 消</el-button>
        <el-button type="primary" @click="submitMoveRequirement()">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  created () {
    // 获取上一页传递过来的Id和Name
    this.projectId = this.$route.query.projectId
    this.projectName = this.$route.query.projectName
    this.currentNodeKey = this.$route.query.requirementId
    // 获取需求树
    this.getRequirementTree()
  },
  data () {
    return {
      dialogVisible: {
        moveRequirement: false
      },
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
      ],
      // 移动用的Tress
      moveRequirementTree: [],
      moveDefaultExpandedKey: [],
      tmpMoveDetails: {
        requirementId: '',
        baseId: '',
        location: ''
      }
    }
  },
  methods: {
    // 刷新当前页面（F5刷新）
    fresh () {
      location.reload()
    },
    async getRequirementTree () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/requirement/tree/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: this.projectId
        }
      })
      if (res.meta.status === 200) {
        this.requirementTree = res.data
        setTimeout(() => {
          this.$refs.requirementTreeRef.setCurrentKey(this.currentNodeKey)
        }, 100)
        this.defaultExpandedKey = [this.currentNodeKey]
      } else {
        // this.$message.error(res.meta.msg)
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
        path: '/requirements/requirementHomepage',
        query: {
          projectId: this.projectId,
          projectName: this.projectName,
          requirementId: requirementId
        }
      })
    },
    handleAddRequirement (command) {
      if (command === 'importFile') {
        // 跳转至导入需求页面
        this.$router.push({
          path: '/requirements/importRequirementDoc',
          query: {
            projectId: this.projectId,
            projectName: this.projectName
          }
        })
      } else {
        var baseId = this.currentNodeKey
        var location = ''
        // 如果baseId是空，则直接返回
        if (!baseId) return this.$message.error('请选择添加的位置！')
        if (command === 'addBefore') {
          location = 'before'
        } else if (command === 'addAfter') {
          location = 'after'
        } else if (command === 'addInner') {
          location = 'inner'
        }
        if (['2', '3', '4', '7'].includes(baseId) && location !== 'inner') {
          return this.$message.error('请选择正确的位置！')
        }
        // 跳转至添加需求页面
        this.$router.push({
          path: '/requirements/addSingleRequirement',
          query: {
            projectId: this.projectId,
            projectName: this.projectName,
            baseId: baseId,
            location: location
          }
        })
      }
    },
    handleMoveRequirement () {
      // 检查是否可以删除
      if (!this.currentNodeKey) return this.$message.error('请选择要移动的需求！')
      if (['2', '3', '4', '7'].includes(this.currentNodeKey)) {
        return this.$message.error('无法移动需求类型！')
      }
      // 深拷贝数组
      this.moveRequirementTree = JSON.parse(JSON.stringify(this.requirementTree))
      // https://blog.csdn.net/lonewoif/article/details/87926144
      setTimeout(() => {
        this.$refs.moveRequirementTreeRef.setCurrentKey(this.currentNodeKey)
      }, 100)
      this.moveDefaultExpandedKey = [this.currentNodeKey]
      this.dialogVisible.moveRequirement = true
    },
    allowDrag (node) {
      if (['2', '3', '4', '7'].includes(node.data._id)) {
        return false
      }
      return node.data._id === this.currentNodeKey
    },
    allowDrop (draggingNode, dropNode, type) {
      if (['2', '3', '4', '7'].includes(dropNode.data._id) && type !== 'inner') {
        return false
      }
      return true
    },
    handleNodeDrop (draggingNode, dropNode, location) {
      this.tmpMoveDetails.requirementId = draggingNode.data._id
      this.tmpMoveDetails.baseId = dropNode.data._id
      this.tmpMoveDetails.location = location
      // https://blog.csdn.net/lonewoif/article/details/87926144
      setTimeout(() => {
        this.$refs.moveRequirementTreeRef.setCurrentKey(this.currentNodeKey)
      }, 100)
    },
    async submitMoveRequirement () {
      const { data: res } = await this.$http({
        method: 'put',
        url: '/requirement/tree/edit',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          project_id: this.$route.query.projectId,
          requirement_id: this.tmpMoveDetails.requirementId,
          base_id: this.tmpMoveDetails.baseId,
          location: this.tmpMoveDetails.location
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.dialogVisible.moveRequirement = false
        this.getRequirementTree()
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    deleteRequirement () {
      var node = this.$refs.requirementTreeRef.getCurrentNode()
      // 如果没有选择任何节点，则返回
      if (!node) return this.$message.error('请选择删除的需求条目！')
      // 如果是需求分类节点，直接返回
      if (['2', '3', '4', '7'].includes(node._id)) {
        return this.$message.error('无法删除需求类型！')
      }
      // 判断是否为叶子节点
      if (node.children.length !== 0) {
        return this.$message.error('该需求下仍有需求，无法删除！')
      }
      this.$messageBox('此操作将永久删除该需求, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http({
          method: 'delete',
          url: '/requirement/delete',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            requirement_id: this.currentNodeKey
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.getRequirementTree()
          // 跳转到项目主页
          this.$router.push({
            path: '/projects/projectHomepage',
            query: { projectId: this.projectId, projectName: this.projectName }
          })
        } else {
          this.$message.error(res.meta.msg)
        }
      }).catch(() => {
        this.$message({ type: 'info', message: '已取消删除' })
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
