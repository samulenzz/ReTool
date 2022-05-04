<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 登录Logo -->
      <div class="login-logo">
        <img src="../assets/login.png">
      </div>
      <!-- 登录表单 -->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" class="login-form">
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="el-icon-user-solid" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" placeholder="请输入密码" clearable type="password"></el-input>
        </el-form-item>
        <!-- 按钮 -->
        <el-form-item class="login-buttons">
          <el-button type="primary" @click="login">登录</el-button>
        </el-form-item>
      </el-form>
      <!-- 注册表单 -->
      <el-button type="primary" @click="handleRegister()">注册</el-button>
    </div>

    <!-- 对话框区 -->
    <!-- 添加用户对话框 -->
    <el-dialog title="添加用户" :visible.sync="dialogVisiable.register" width="30%">
      <el-form label-position="right" label-width="80px" :model="userForm"
        ref="registerFormRef" :rules="userFormRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="初始密码" prop="password">
          <el-input type="password" v-model="userForm.password" placeholder="请输入初始密码"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱（可选）"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="phone_number">
          <el-input v-model="userForm.phone_number" placeholder="请输入电话（可选）"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.register = false">取 消</el-button>
        <el-button type="primary" @click="register()">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  data () {
    return {
      // 对话框是否可见
      dialogVisiable: {
        register: false
      },
      // 注册表单的数据对象
      userForm: {
        username: '',
        password: '',
        email: '',
        phone_number: ''
      },
      // 注册表单的前端校验
      userFormRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' }
        ],
        email: [
          { required: false }
        ],
        phone_number: [
          { required: false }
        ]
      },
      // 登录表单的数据对象
      loginForm: {
        username: '',
        password: ''
      },
      // 登录表单前端校验
      loginFormRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    login () {
      this.$refs.loginFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http.post('/login', this.loginForm)
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        else {
          this.$message.success(res.meta.msg)
          // 登录成功后：
          // 1. 将token存储至session storage
          window.sessionStorage.setItem('token', res.data.token)
          window.sessionStorage.setItem('username', this.loginForm.username)
          // 2. 跳转到/home 页面
          this.$router.push('/home')
        }
      })
    },
    clearUserForm () {
      this.userForm.username = ''
      this.userForm.password = ''
      this.userForm.email = ''
      this.userForm.phone_number = ''
    },
    handleRegister () {
      this.dialogVisiable.register = true
      this.clearUserForm()
    },
    register () {
      this.$refs.registerFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'post',
          url: '/register',
          data: {
            username: this.userForm.username,
            password: this.userForm.password,
            system_role: '系统用户',
            email: this.userForm.email,
            phone_number: this.userForm.phone_number
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.dialogVisiable.register = false
        } else {
          this.$message.error(res.meta.msg)
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login-container {
  background-image: linear-gradient(left top, #ccfbff, #ef96c5);
  height: 100%;
}

.login-box {
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  .login-logo {
    width: 220px;
    height: 80px;
    position: absolute;
    left: 50%;
    top: 20px;
    transform: translate(-50%);

    img {
      height: 100%;
      width: 100%;
    }
  }

  .login-form {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;

    .login-buttons {
      text-align: center;
    }
  }
}
</style>
