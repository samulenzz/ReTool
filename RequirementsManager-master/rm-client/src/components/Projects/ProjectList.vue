<template>
  <div class="main-container">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item>项目列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 顶部搜索添加区 -->
      <el-row :gutter="20">
        <!--<el-col :span="8">
          <el-input placeholder="请输入项目名称关键字" class="input">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>-->
        <el-col :span="4">
          <el-button type="primary" @click="addProject()">创建项目</el-button>
        </el-col>
      </el-row>
      <!-- 表格主题区 -->
      <el-table class="project-table" :data="projectList" border>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="projectName" label="项目名称" >
          <template slot-scope="scope">
            <div @click="jumpToProjectHomepage(scope.row.projectId, scope.row.projectName)"
            class="project-name-col" >{{scope.row.projectName}}</div>
          </template>
        </el-table-column>
        <el-table-column prop="projectStatus" label="项目状态"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip class="item" effect="light" content="项目信息" placement="top-start">
              <el-button type="primary" size="small" icon="el-icon-setting" @click="projectInfo(scope.row.projectId)"></el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="light" content="删除项目" placement="top-start">
              <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteProject(scope.row.projectId)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  created () {
    this.getProjectList()
  },
  data () {
    return {
      projectList: []
    }
  },
  methods: {
    async getProjectList () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/project/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          username: window.sessionStorage.getItem('username')
        }
      })
      if (res.meta.status === 200) {
        this.projectList = []
        // 遍历结果数组，赋值给 projectList
        for (let i = 0; i < res.data.length; i++) {
          this.projectList.push(
            {
              projectId: res.data[i]._id,
              projectName: res.data[i].project_name,
              projectStatus: res.data[i].status
            }
          )
        }
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    addProject () {
      this.$router.push('/projects/addProject')
    },
    projectInfo (projectId) {
      this.$router.push({ path: '/projects/projectProfile', query: { projectId: projectId } })
    },
    deleteProject (projectId) {
      this.$messageBox('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http({
          method: 'delete',
          url: '/project/delete',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            project_id: projectId
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.getProjectList()
        } else {
          this.$message.error(res.meta.msg)
        }
      }).catch(() => {
        this.$message({ type: 'info', message: '已取消删除' })
      })
    },
    jumpToProjectHomepage (projectId, projectName) {
      this.$router.push({
        path: '/projects/projectHomepage',
        query: { projectId: projectId, projectName: projectName }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.project-table {
  margin-top: 15px;
}

.project-name-col {
  cursor: pointer;
}
</style>
