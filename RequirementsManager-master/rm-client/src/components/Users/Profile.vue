<template>
  <div class="main-container" style="overflow: auto;">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>个人信息</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 个人信息表单区域 -->
    <el-card class="box-card">
      <el-form class="profile-form" :rules="profileFormRules" ref="profileFormRef"
        :model="profileForm" label-width="120px" label-position="right">
        <el-form-item label="用户名" prop="username">
          <el-input type="primary" v-model="profileForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input type="primary" v-model="profileForm.email"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input type="primary" v-model="profileForm.phoneNumber"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitProfileForm()">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  created () {
    this.getProfile()
  },
  data () {
    var isEmail = (rule, value, callback) => {
      if (!value) {
        callback()
      } else {
        const reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        const email = reg.test(value)
        if (!email) {
          callback(new Error('邮箱格式如:admin@163.com'))
        } else {
          callback()
        }
      }
    }
    return {
      profileForm: {
        username: '',
        email: '',
        phoneNumber: ''
      },
      profileFormRules: {
        email: [
          { validator: isEmail, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async getProfile () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/user/profile',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          username: this.$route.query.username
        }
      })
      if (res.meta.status === 200) {
        this.profileForm.username = res.data.username
        this.profileForm.email = res.data.email
        this.profileForm.phoneNumber = res.data.phone_number
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    submitProfileForm () {
      this.$refs.profileFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'put',
          url: '/user/edit',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            username: this.profileForm.username,
            email: this.profileForm.email,
            phone_number: this.profileForm.phoneNumber
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
.profile-form {
  position: relative;
  width: 400px;
}
</style>
