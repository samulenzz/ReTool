<template>
  <div class="main-container">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>工具箱</el-breadcrumb-item>
        <el-breadcrumb-item>模糊检测</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 顶部搜索添加区 -->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input placeholder="请输入文档名称关键字" class="input">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addFile()">上传文档</el-button>
        </el-col>
      </el-row>
      <!-- 表格主题区 -->
      <el-table class="project-table" :data="fileList" border>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="fileName" label="文档名称" ></el-table-column>
        <el-table-column prop="fileDescription" label="文档描述"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip class="item" effect="light" content="上传文件" placement="top-start">
              <el-button type="info" size="small" icon="el-icon-upload" @click="importFile(scope.row.fileId,scope.row.fileName)"></el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="light" content="模糊语句检测" placement="top-start">
              <el-button type="primary" size="small" icon="el-icon-search" @click="importFile(scope.row.fileId)"></el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="light" content="模糊传播检测" placement="top-start">
              <el-button type="success" size="small" icon="el-icon-search" @click="projectInfo(scope.row.projectId)"></el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="light" content="删除文档" placement="top-start">
              <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteFile(scope.row.fileId)"></el-button>
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
    this.getFileList()
  },
  data () {
    return {
      fileList: []
    }
  },
  methods: {
    async getFileList () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/file/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          username: window.sessionStorage.getItem('username')
        }
      })
      if (res.meta.status === 200) {
        this.fileList = []
        // 遍历结果数组，赋值给 projectList
        for (let i = 0; i < res.data.length; i++) {
          this.fileList.push(
            {
              fileId: res.data[i]._id,
              fileName: res.data[i].file_name,
              fileDescription: res.data[i].description
            }
          )
        }
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    importFile (fileid, filename) {
      this.$router.push({
        path: '/tools/importFileDoc',
        query: {
          fileId: fileid,
          fileName: filename
        }
      })
    },
    addFile () {
      this.$router.push('/tools/importFileDoc')
    },
    projectInfo (projectId) {
      this.$router.push({ path: '/projects/projectProfile', query: { projectId: projectId } })
    },
    deleteFile (FileId) {
      this.$messageBox('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http({
          method: 'delete',
          url: '/file/delete',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            file_id: FileId
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
