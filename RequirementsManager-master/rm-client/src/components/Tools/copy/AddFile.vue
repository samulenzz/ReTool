<template>
  <div>
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模糊检测</el-breadcrumb-item>
        <el-breadcrumb-item>创建文档</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 主体 -->
      <el-tabs v-model="activeIndex" tab-position="left" style="overflow: auto;"
        :before-leave="beforeTabLeave">
        <!-- 项目信息 -->
        <el-tab-pane label="文档信息" name="0">
          <el-form class="project-form" label-position="top" label-width="100px" :model="projectForm"
            ref="projectFormRef" :rules="projectFormRules">
            <el-form-item label="文档名称" prop="fileName">
              <el-input v-model="projectForm.fileName"></el-input>
            </el-form-item>
            <el-form-item label="文档描述">
              <el-input v-model="projectForm.description" type="textarea" :rows="3"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="createFile()">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  created () {
    this.getUserList()
  },
  data () {
    return {
      activeIndex: '0',
      dialogVisiable: {
        editProjectRole: false
      },
      // 是否允许切换Tab
      isAllowTabLeave: false,
      projectForm: {
        fileName: '',
        description: ''
      },
      projectFormRules: {
        projectName: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      },
      // 系统中所有用户
      userList: [],
      // 查询框中新添加的用户
      newProjectUser: '',
      // 修改用户角色表单
      editProjectRoleForm: {
        username: '',
        projectRole: ''
      },
      editProjectRoleFormRules: {
        projectRole: { required: true, message: '请选择角色', trigger: 'change' }
      },
      // 项目内的用户
      projectUsers: [
        {
          username: window.sessionStorage.getItem('username'),
          projectRole: '文档编写'
        }
      ]
    }
  },
  methods: {
    async getUserList () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/user/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        }
      })
      if (res.meta.status === 200) {
        this.userList = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 阻止标签页切换
    beforeTabLeave (newActive, oldActive) {
      if (oldActive === '0' && newActive === '1') {
        this.$refs.projectFormRef.validate(valid => {
          if (!valid) {
            this.$message.error('请完成项目信息！')
            this.isAllowTabLeave = false
          } else {
            this.isAllowTabLeave = true
          }
        })
      }
      return this.isAllowTabLeave
    },
    submitProjectInfo () {
      this.beforeTabLeave('1', '0')
      if (this.isAllowTabLeave === true) {
        this.activeIndex = '1'
      }
    },
    addUser () {
      // 检查是否为空
      if (this.newProjectUser === '') return
      // 检查该用户是否已经存在
      for (let i = 0; i < this.projectUsers.length; i++) {
        if (this.projectUsers[i].username === this.newProjectUser) {
          this.$message.error('该用户已存在！')
          return
        }
      }
      this.projectUsers.push({
        username: this.newProjectUser,
        projectRole: '普通成员'
      })
    },
    handleEditProjectRole (username) {
      this.editProjectRoleForm.username = username
      this.dialogVisiable.editProjectRole = true
    },
    editProjectRole () {
      this.$refs.editProjectRoleFormRef.validate(async valid => {
        if (!valid) return
        for (let i = 0; i < this.projectUsers.length; i++) {
          if (this.projectUsers[i].username === this.editProjectRoleForm.username) {
            this.projectUsers[i].projectRole = this.editProjectRoleForm.projectRole
            this.dialogVisiable.editProjectRole = false
            break
          }
        }
      })
    },
    deleteUser (username) {
      for (var i = 0; i < this.projectUsers.length; i++) {
        if (this.projectUsers[i].username === username) {
          break
        }
      }
      this.projectUsers.splice(i, 1)
    },
    async createFile () {
      // 准备用户列表
      var users = []
      for (let i = 0; i < this.projectUsers.length; i++) {
        users.push({
          username: this.projectUsers[i].username,
          project_role: this.projectUsers[i].projectRole
        })
      }
      // 准备body
      var body = {
        file_name: this.projectForm.fileName,
        description: this.projectForm.description
      }
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: body
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.$router.push('/tools/fileList')
      } else {
        this.$message.error(res.meta.msg)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.project-form {
  width: 800px;
}
</style>
