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
        <el-breadcrumb-item>上传文档开始检测</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 头部步骤条区 -->
      <el-alert title="模糊检测" type="info" center show-icon></el-alert>

      <!-- 主体区 -->
      <el-tabs v-model="activeIndex" tab-position="top" stretch=true style="overflow: auto;position:relative;">
        <el-tab-pane label="填写基本信息" name="0" class="center">
          <el-form class="project-form" label-position="left" label-width="120px" :model="projectForm"
            ref="projectFormRef" :rules="projectFormRules" style="margin:auto;">
            <el-form-item label="请输入文档名称:" prop="fileName" style="margin-top:20px">
              <el-input v-model="projectForm.fileName"></el-input>
            </el-form-item>
            <el-form-item label="请输入文档描述:" style="margin-top:80px">
              <el-input v-model="projectForm.description" type="textarea" :rows="2"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="createFile()"
              style="margin-top: 10px;position:relative;left:35%;width:10%;padding-left:14px;">
                <span style="position:relative;">保存</span>
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="上传需求文档" name="1" class="center">
          <el-tag v-for="tag in uploadFileTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentUploadFileTag"
          style="margin-left: 10px;">{{tag.name}}</el-tag>
          <el-upload style="margin-top:50px;position:relative;left:32%;width:36%;"
          action="" :multiple="false" :limit="1" drag
          :http-request="addUploadFile" :on-remove="removeUploadFile" :auto-upload="true">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击选取文件</em></div>
            <div slot="tip" style="margin-top:10px;margin-bottom:10px;position:relative;left:33%;width:38%;" class="el-upload__tip">只能上传doc/docx文件</div>
          </el-upload>
          <el-button style="margin-top:30px;margin-bottom:50px;position:relative;left:45%;width:10%;" type="primary" @click="submitUploadFile">上传</el-button>
        </el-tab-pane>
        <!-- 模糊语句检测 -->
        <el-tab-pane label="模糊语句检测" name="2">
          <el-tag v-for="tag in itemizeTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentDetectTag"
          style="margin-left: 10px;">{{tag.name}}</el-tag>
          <p></p>
          <el-scrollbar style="height:100%;position:relative;left:8%;">
            <div style="width:800px;height:400px;border:solid;overflow-x:auto;" >
              <span v-html="uncertainoutput"></span>
            </div>
          </el-scrollbar>
          <el-button type="success" @click="submitUncertainDetect" style="position:relative;left:27%;">开始模糊语句检测</el-button>
          <el-button type="primary" @click="gotoFileList" style="margin-top: 20px;position:relative;left:27%;">保存结果并退出</el-button>
          <el-button type="warning" @click="nextstep()" style="margin-top: 20px;position:relative;left:27%;">下一步</el-button>
        </el-tab-pane>
        <el-tab-pane label="上传结构化信息与需求关联关系" name="3">
          <el-upload style="margin-top:10px;position:relative;left:32%;width:36%;"
          action="" :multiple="false" :limit="1" drag
          :http-request="addStruFile" :on-remove="removeStruFile" :auto-upload="true">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击选取文件</em></div>
            <div slot="tip" style="margin-top:10px;margin-bottom:10px;position:relative;left:33%;width:50%;" class="el-upload__tip">于此处添加需求结构化信息</div>
          </el-upload>
          <el-upload style="margin-top:10px;position:relative;left:32%;width:36%;"
          action="" :multiple="false" :limit="1" drag
          :http-request="addRelaFile" :on-remove="removeRelaFile" :auto-upload="true">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击选取文件</em></div>
            <div slot="tip" style="margin-top:10px;margin-bottom:10px;position:relative;left:33%;width:50%;" class="el-upload__tip">于此处添加需求关联关系</div>
          </el-upload>
          <el-button style="margin-top:10px;margin-bottom:50px;position:relative;left:45%;width:10%;" type="primary" @click="submitUploadFile2">上传</el-button>
        </el-tab-pane>
        <!-- 模糊传播分析 -->
        <el-tab-pane label="模糊传播分析" name="4">
          <el-tag v-for="tag in itemizeTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentDetectTag"
          style="margin-left: 10px;">{{tag.name}}</el-tag>
          <p></p>
          <el-scrollbar style="height:100%;position:relative;left:8%;">
            <div style="width:800px;height:400px;border:solid;overflow-x:auto;" >
              <span v-html="spreadoutput"></span>
            </div>
          </el-scrollbar>
          <el-button type="success" @click="submitSpreadDetect" style="position:relative;left:33%;">开始模糊传播分析</el-button>
          <el-button type="primary" @click="gotoFileList" style="margin-top: 20px;position:relative;left:33%;">保存结果并退出</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      mystyle: {
        margin: 'auto',
        position: 'absolute',
        top: '0',
        left: '0',
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
      fileId: 'wzd',
      uncertainoutput: '',
      spreadoutput: '',
      projectsName: 'MyProject',
      activeIndex: '0',
      activeAnalyzeIndex: '0',
      uploadFile: null,
      struFile: null,
      relaFile: null,
      uploadFileToken: '',
      currentUploadFileTag: '',
      uploadFileTags: [
        { name: '上传中', type: 'primary' },
        { name: '上传成功', type: 'success' },
        { name: '上传失败', type: 'danger' }
      ],
      currentDetectTag: '',
      itemizeTags: [
        { name: '模糊语句检测中，请稍后...', type: 'primary' },
        { name: '模糊语句检测成功', type: 'success' },
        { name: '模糊语句检测失败', type: 'danger' }
      ]
    }
  },
  methods: {
    async createFile () {
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
        this.activeIndex = '1'
        this.fileId = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 检测需求是否被填写完成
    beforeTabLeave (newActive, oldActive) {
      if (newActive === '2' && oldActive !== '2') {
        if (this.requirementTree.length === 0) {
          this.$message.error('请完成上传文件和条目化！')
          return false
        } else {
          return true
        }
      }
      return true
    },
    // 下一步
    nextstep () {
      if (this.activeIndex === '0') {
        this.activeIndex = '1'
      } else if (this.activeIndex === '1') {
        this.activeIndex = '2'
      } else if (this.activeIndex === '2') {
        this.activeIndex = '3'
      } else if (this.activeIndex === '3') {
        this.activeIndex = '4'
      } else if (this.activeIndex === '4') {
        this.activeIndex = '5'
      }
    },
    // 返回文件列表
    gotoFileList () {
      this.$router.push('/tools/FileList')
    },
    // 添加文件
    addUploadFile (file) {
      this.uploadFile = file.file
      this.currentUploadFileTag = ''
    },
    addStruFile (file) {
      this.struFile = file.file
      this.currentUploadFileTag = ''
    },
    addRelaFile (file) {
      this.relaFile = file.file
      this.currentUploadFileTag = ''
    },
    // 移除文件
    removeUploadFile (file) {
      this.uploadFile = null
      this.currentUploadFileTag = ''
    },
    removeStruFile (file) {
      this.struFile = null
      this.currentUploadFileTag = ''
    },
    removeRelaFile (file) {
      this.relaFile = null
      this.currentUploadFileTag = ''
    },
    async submitUploadFile () {
      if (!this.uploadFile) return this.$message.error('请导入文件！')
      var formData = new FormData()
      formData.append('file', this.uploadFile)
      formData.append('fileid', this.fileId)
      this.currentUploadFileTag = '上传中,请稍候'
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/importfile/upload',
        headers: {
          'Authorization': window.sessionStorage.getItem('token'),
          'Content-type': 'application/x-www-form-urlencoded'
        },
        /*
        data: {
          file_id: this.fileId,
          formData: formData
        }
        */
        data: formData
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.uploadFileToken = res.data.token
        this.currentUploadFileTag = '上传成功'
        this.activeIndex = '2'
      } else {
        this.$message.error(res.meta.msg)
        this.currentUploadFileTag = '上传失败'
      }
    },
    async submitUploadFile2 () {
      this.currentDetectTag = ''
      if (!this.struFile) return this.$message.error('请导入文件！')
      if (!this.relaFile) return this.$message.error('请导入文件！')
      var formData = new FormData()
      formData.append('strufile', this.struFile)
      formData.append('relafile', this.relaFile)
      formData.append('fileid', this.fileId)
      this.currentUploadFileTag = '上传中,请稍候'
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/importfile/upload2',
        headers: {
          'Authorization': window.sessionStorage.getItem('token'),
          'Content-type': 'application/x-www-form-urlencoded'
        },
        data: formData
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.currentUploadFileTag = '上传成功'
        this.activeIndex = '4'
      } else {
        this.$message.error(res.meta.msg)
        this.currentUploadFileTag = '上传失败'
      }
    },
    // 模糊检测
    async submitUncertainDetect () {
      if (!this.uploadFileToken) return this.$message.error('请先上传文件！')
      this.currentDetectTag = '模糊语句检测中，请稍后...'
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/importfile/uncertaindetect',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          fileId: this.fileId,
          uploadFileToken: this.uploadFileToken
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.currentDetectTag = '模糊语句检测成功'
        this.uncertainoutput = res.data
      } else {
        this.$message.error(res.meta.msg)
        this.currentDetectTag = '模糊语句检测失败'
      }
    },
    // 模糊传播分析
    async submitSpreadDetect () {
      this.currentDetectTag = '模糊传播分析中，请稍后...'
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/importfile/spreaddetect',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          fileId: this.fileId
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.currentDetectTag = '模糊传播分析成功'
        this.spreadoutput = res.data
      } else {
        this.$message.error(res.meta.msg)
        this.currentDetectTag = '模糊传播分析失败'
      }
    }
  }
}
</script>

<style lang="less" scoped>
.el-form {
  width: 70%;
}
.center {
/*
  margin: auto;
  width: 60%;
  padding: 10px;
*/
  position:relative;
  margin:auto;
}
</style>

<style lang="less">
/* 必须设置成全局，去掉scoped */
/* 参考：https://segmentfault.com/q/1010000017251094 */
.analyze-table-form label {
  color: #99a9bf
}
</style>
