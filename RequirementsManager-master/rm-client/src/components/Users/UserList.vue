<template>
  <div>
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 搜索与添加区域 -->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input placeholder="请输入用户名关键字" class="input">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleAddUser()">添加用户</el-button>
        </el-col>
      </el-row>
      <!-- 用户表格区 -->
      <el-table class="user-table" :data="userList" border>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="system_role" label="系统角色"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="light" content="修改角色" placement="top-start">
              <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEditSysRole(scope.row.username)"></el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="重置密码" placement="top-start">
              <el-button type="warning" size="small" icon="el-icon-unlock" @click="handleEditPasswrd(scope.row.username)"></el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="删除用户" placement="top-start">
              <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteUser(scope.row.username)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 对话框区 -->
    <!-- 添加用户对话框 -->
    <el-dialog title="添加用户" :visible.sync="dialogVisiable.addUser" width="30%">
      <el-form label-position="right" label-width="80px" :model="userForm"
        ref="addUserFormRef" :rules="userFormRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="初始密码" prop="password">
          <el-input type="password" v-model="userForm.password" placeholder="请输入初始密码"></el-input>
        </el-form-item>
        <el-form-item label="系统角色" prop="sysRole">
          <el-select v-model="userForm.sysRole" placeholder="请选择系统角色">
            <el-option label="系统管理员" value="系统管理员"></el-option>
            <el-option label="系统用户" value="系统用户"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.addUser = false">取 消</el-button>
        <el-button type="primary" @click="addUser()">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改角色 -->
    <el-dialog title="修改角色" :visible.sync="dialogVisiable.editSysRole" width="30%">
      <el-form label-position="right" label-width="80px" :model="userForm"
        :rules="userFormRules" ref="editSysRoleFormRef">
        <el-form-item label="用户名">
          <el-input v-model="userForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="系统角色" prop="sysRole">
          <el-select v-model="userForm.sysRole" placeholder="请选择系统角色">
            <el-option label="系统管理员" value="系统管理员"></el-option>
            <el-option label="系统用户" value="系统用户"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.editSysRole = false">取 消</el-button>
        <el-button type="primary" @click="editSysRole()">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 重置密码 -->
    <el-dialog title="重置密码" :visible.sync="dialogVisiable.editPassword" width="30%">
      <el-form label-position="right" label-width="80px" :model="userForm"
        ref="editPasswordFormRef" :rules="userFormRules">
        <el-form-item label="用户名">
          <el-input v-model="userForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="重置密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请重置密码"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.editPassword = false">取 消</el-button>
        <el-button type="primary" @click="editPassword()">确 定</el-button>
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
      dialogVisiable: {
        addUser: false,
        editSysRole: false,
        editPassword: false
      },
      userForm: {
        username: '',
        password: '',
        sysRole: ''
      },
      userFormRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' }
        ],
        sysRole: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      },
      userList: []
    }
  },
  methods: {
    clearUserForm () {
      this.userForm.username = ''
      this.userForm.password = ''
      this.userForm.sysRole = ''
    },
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
    handleAddUser () {
      this.dialogVisiable.addUser = true
      this.clearUserForm()
    },
    addUser () {
      this.$refs.addUserFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'post',
          url: '/user/create',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: this.userForm.username,
            password: this.userForm.password,
            system_role: this.userForm.sysRole
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.dialogVisiable.addUser = false
          this.getUserList()
        } else {
          this.$message.error(res.meta.msg)
        }
      })
    },
    handleEditSysRole (username) {
      this.clearUserForm()
      this.userForm.username = username
      this.dialogVisiable.editSysRole = true
    },
    editSysRole () {
      this.$refs.editSysRoleFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'put',
          url: '/user/edit',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: this.userForm.username,
            system_role: this.userForm.sysRole
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.dialogVisiable.editSysRole = false
          this.getUserList()
        } else {
          this.$message.error(res.meta.msg)
        }
      })
    },
    handleEditPasswrd (username) {
      this.clearUserForm()
      this.userForm.username = username
      this.dialogVisiable.editPassword = true
    },
    editPassword () {
      this.$refs.editPasswordFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'put',
          url: '/user/edit',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: this.userForm.username,
            password: this.userForm.password
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.dialogVisiable.editPassword = false
          this.getUserList()
        } else {
          this.$message.error(res.meta.msg)
        }
      })
    },
    deleteUser (username) {
      this.$messageBox('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http({
          method: 'delete',
          url: '/user/delete',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: username
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.getUserList()
        } else {
          this.$message.error(res.meta.msg)
        }
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  }
}
</script>

<style lang="less" scoped>
.user-table {
  margin-top: 15px;
}
</style>
