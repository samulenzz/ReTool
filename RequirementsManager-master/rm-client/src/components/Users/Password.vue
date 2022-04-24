<template>
  <div class="main-container" style="overflow: auto;">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>修改密码</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 修改密码表单区域 -->
    <el-card class="box-card">
      <el-form class="password-form" :rules="passwordFormRules" ref="passwordFormRef"
        :model="passwordForm" label-width="120px" label-position="right">
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="checkPassword">
          <el-input type="password" v-model="passwordForm.checkPassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitPasswordForm()">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    var validateCheckPassword = (rule, value, callback) => {
      if (!value) {
        callback()
      } else {
        if (value !== this.passwordForm.newPassword) {
          callback(new Error('两次密码不一致！'))
        } else {
          callback()
        }
      }
    }
    return {
      passwordForm: {
        newPassword: '',
        checkPassword: ''
      },
      passwordFormRules: {
        newPassword: [
          { required: true, min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' }
        ],
        checkPassword: [
          { required: true, min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' },
          { validator: validateCheckPassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitPasswordForm () {
      this.$refs.passwordFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'put',
          url: '/user/edit',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: this.$route.query.username,
            password: this.passwordForm.newPassword
          }
        })
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        else {
          this.$message.success(res.meta.msg)
        }
      })
    }
  }
}
</script>

<style>
.password-form {
  position: relative;
  width: 400px;
}
</style>
