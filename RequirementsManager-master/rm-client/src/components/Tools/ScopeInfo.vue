<template>
  <div>
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>工具箱</el-breadcrumb-item>
        <el-breadcrumb-item :to="{
          path: '/tools/FileList'
        }">模糊检测</el-breadcrumb-item>
        <el-breadcrumb-item>{{this.$route.query.fileName}}</el-breadcrumb-item>
        <el-breadcrumb-item>模糊语句检测结果</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div :style="mystyle">
      <el-scrollbar style="height:100%">
        <div style="width:850px;height:600px;border:solid;overflow-x:auto;" >
          <span v-html="uncertainoutput"></span>
        </div>
      </el-scrollbar>
    </div>
    <el-button type="success" @click="gotoFileList()" style="margin-top: 10px;margin-left: 12px;">返回</el-button>
  </div>
</template>

<script>
export default {
  created () {
    this.getScope()
  },
  data () {
    return {
      mystyle: {
        margin: 'auto',
        position: 'absolute',
        top: '9%',
        left: '28%',
        right: '0',
        bottom: '0'
      },
      projectForm: {
        fileName: '',
        description: ''
      },
      projectFormRules: {
        projectName: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      },
      uncertainoutput: ''
    }
  },
  methods: {
    // 返回文件列表
    gotoFileList () {
      this.$router.push('/tools/FileList')
    },
    async getScope () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/file/getscope',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          file_id: this.$route.query.fileId
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.uncertainoutput = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.el-form {
  width: 70%;
}
</style>

<style lang="less">
/* 必须设置成全局，去掉scoped */
/* 参考：https://segmentfault.com/q/1010000017251094 */
.analyze-table-form label {
  color: #99a9bf
}
</style>
