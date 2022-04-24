<template>
  <div>
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item>创建项目</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 头部步骤条区 -->
      <el-alert title="新建项目" type="info" center></el-alert>
      <el-steps :active="activeIndex - 0" align-center>
        <el-step title="项目信息"></el-step>
        <el-step title="添加成员"></el-step>
      </el-steps>
      <!-- 主体 -->
      <el-tabs v-model="activeIndex" tab-position="left" style="overflow: auto;"
        :before-leave="beforeTabLeave">
        <!-- 项目信息 -->
        <el-tab-pane label="项目信息" name="0">
          <el-form class="project-form" label-position="top" label-width="100px" :model="projectForm"
            ref="projectFormRef" :rules="projectFormRules">
            <el-form-item label="项目名称" prop="projectName">
              <el-input v-model="projectForm.projectName"></el-input>
            </el-form-item>
            <el-form-item label="项目描述">
              <el-input v-model="projectForm.description" type="textarea" :rows="3"></el-input>
            </el-form-item>
            <el-form-item label="项目状态">
              <el-select v-model="projectForm.status" placeholder="请选择项目状态">
                <el-option label="未开始" value="未开始"></el-option>
                <el-option label="进行中" value="进行中"></el-option>
                <el-option label="已结束" value="已结束"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitProjectInfo()">下一步</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <!-- 添加成员 -->
        <el-tab-pane label="添加成员" name="1">
          <!-- 顶部区域 -->
          <el-row :gutter="10">
            <el-col :span="4">
              <el-select v-model="newProjectUser" filterable placeholder="请输入用户名">
                <el-option v-for="user in userList" :key="user.username" :label="user.username" :value="user.username">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="1">
              <el-button type="primary" @click="addUser()">添加用户</el-button>
            </el-col>
          </el-row>
          <!-- 用户表格区 -->
          <el-table ref="projectUsersRef" :data="projectUsers">
            <el-table-column type="index"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="projectRole" label="项目角色"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-tooltip effect="light" content="修改项目角色" placement="top-start">
                  <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEditProjectRole(scope.row.username)"></el-button>
                </el-tooltip>
                <el-tooltip effect="light" content="删除用户" placement="top-start">
                  <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteUser(scope.row.username)"></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <!-- 确认按钮区 -->
          <el-button type="primary" @click="createProject()" style="margin-top: 20px;">创建项目</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- Dialog区 -->
    <!-- 修改角色 -->
    <el-dialog title="修改角色" :visible.sync="dialogVisiable.editProjectRole" width="30%">
      <el-form label-position="right" label-width="80px" :model="editProjectRoleForm"
        :rules="editProjectRoleFormRules" ref="editProjectRoleFormRef">
        <el-form-item label="用户名">
          <el-input v-model="editProjectRoleForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="项目角色" prop="projectRole">
          <el-select v-model="editProjectRoleForm.projectRole" placeholder="请选择项目角色">
            <el-option label="项目经理" value="项目经理"></el-option>
            <el-option label="项目组长" value="项目组长"></el-option>
            <el-option label="普通成员" value="普通成员"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.editProjectRole = false">取 消</el-button>
        <el-button type="primary" @click="editProjectRole()">确 定</el-button>
      </span>
    </el-dialog>
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
        projectName: '',
        description: '',
        status: ''
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
          projectRole: '项目经理'
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
    async createProject () {
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
        project_name: this.projectForm.projectName,
        description: this.projectForm.description,
        status: this.projectForm.status,
        users: users
      }
      const { data: res } = await this.$http({
        method: 'post',
        url: '/project/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: body
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.$router.push('/projects/projectList')
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
