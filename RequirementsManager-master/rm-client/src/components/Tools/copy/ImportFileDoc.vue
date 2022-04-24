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
        <el-breadcrumb-item>上传文件</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 头部步骤条区 -->
      <el-alert title="上传文件" type="info" center show-icon></el-alert>
      <el-steps :active="activeIndex - 0" align-center>
        <el-step title="上传需求文档"></el-step>
        <el-step title="模糊语句检测"></el-step>
        <el-step title="上传结构化信息与关联关系"></el-step>
        <el-step title="模糊传播分析"></el-step>
      </el-steps>

      <!-- 主体区 -->
      <el-tabs v-model="activeIndex" tab-position="left" style="overflow: auto;"
      :before-leave="beforeTabLeave">
        <el-tab-pane label="上传需求文档" name="0">
          <el-button style="margin-bottom: 10px;" size="small" type="success" @click="submitUploadFile">上传到服务器</el-button>
          <el-tag v-for="tag in uploadFileTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentUploadFileTag"
          style="margin-left: 10px;">{{tag.name}}</el-tag>
          <el-upload action="" :multiple="false" :limit="1" drag
          :http-request="addUploadFile" :on-remove="removeUploadFile" :auto-upload="true">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击选取文件</em></div>
            <div slot="tip" class="el-upload__tip">只能上传doc/docx文件</div>
          </el-upload>
          <el-button type="primary" @click="activeIndex='1'" style="margin-top: 20px;">下一步</el-button>
        </el-tab-pane>
        <!-- 模糊语句检测 -->
        <el-tab-pane label="条目化" name="1">
          <el-button type="success" size="small" @click="submitUncertainDetect">开始模糊语句检测</el-button>
          <el-tag v-for="tag in itemizeTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentDetectTag"
          style="margin-left: 10px;">{{tag.name}}</el-tag>
          <p></p>
          <el-scrollbar style="height:100%">
            <div style="width:400px;height:100px;border:solid;overflow-x:auto;" >
              <span v-html="uncertainoutput"></span>
            </div>
          </el-scrollbar>
        <el-button type="primary" @click="nextstep()" style="margin-top: 20px;">下一步</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      uncertainoutput: '<span style="color:blue">The following problem is<span style="color:red"> supposed</span> to be the participants of the Dagstuhl Meeting</span> .',
      projectsName: 'MyProject',
      activeIndex: '0',
      activeAnalyzeIndex: '0',
      uploadFile: null,
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
      ],
      requirementTree: [],
      // 联级选择需求分析范围
      analyzeScopeProps: {
        lazy: true,
        lazyLoad: this.lazyLoad
      },
      conflictAnalyzeTable: [],
      similarityAnalyzeTable: [],
      relationshipAnalyzeTable: []
    }
  },
  methods: {
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
      if (this.beforeTabLeave('2', '1') === true) {
        if (this.activeIndex === '0') {
          this.activeIndex = '1'
        } else if (this.activeIndex === '1') {
          this.activeIndex = '2'
        }
      }
    },
    // 添加文件
    addUploadFile (file) {
      this.uploadFile = file.file
      this.currentUploadFileTag = ''
    },
    // 移除文件
    removeUploadFile (file) {
      this.uploadFile = null
      this.currentUploadFileTag = ''
    },
    async submitUploadFile () {
      if (!this.uploadFile) return this.$message.error('请导入文件！')
      var formData = new FormData()
      formData.append('file', this.uploadFile)
      this.currentUploadFileTag = '上传中'
      const { data: res } = await this.$http({
        method: 'post',
        url: '/file/importfile/upload',
        headers: {
          'Authorization': window.sessionStorage.getItem('token'),
          'Content-type': 'multipart/form-data'
        },
        data: formData
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.uploadFileToken = res.data.token
        this.currentUploadFileTag = '上传成功'
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
          token: this.uploadFileToken
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
    // 给需求树增添样式
    renderTreeContent (h, { node, data, store }) {
      if (['2', '3', '4', '7'].includes(node.data._id)) {
        return (<span style="font-size: 15px; font-weight: bold;">{node.label}</span>)
      } else return (<span style="font-size: 14px;">{node.label}</span>)
    },
    // 创建需求
    async submitCreateRequirements () {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/requirement/importfile/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          project_id: this.$route.query.projectId,
          tree: this.requirementTree
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.$router.push({
          path: '/projects/projectHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.$route.query.projectName
          }
        })
        this.$emit('fresh')
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 获取项目列表
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
        var projectList = []
        // 遍历结果数组，赋值给 projectList
        for (let i = 0; i < res.data.length; i++) {
          projectList.push(
            {
              projectId: res.data[i]._id,
              projectName: res.data[i].project_name,
              projectStatus: res.data[i].status
            }
          )
        }
        return projectList
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 获取归档版本
    async getBaselineNodes (projectId) {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/project/baseline/node/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: projectId
        }
      })
      if (res.meta.status === 200) {
        var baselineNodes = res.data
        return baselineNodes
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // lazyLoad
    async lazyLoad (node, resolve) {
      // 如果是根节点，直接返回
      var nodes = []
      if (node.level === 0) {
        nodes.push({ value: this.$route.query.projectId, label: '当前项目' })
        var projectList = await this.getProjectList()
        for (let i = 0; i < projectList.length; i++) {
          nodes.push(
            {
              value: projectList[i].projectId,
              label: projectList[i].projectName
            }
          )
        }
      } else if (node.level === 1) {
        nodes.push({ value: null, label: '当前版本', leaf: true })
        nodes.push({ value: node.value, label: '归档版本' })
      } else if (node.level === 2) {
        var baselineNodes = await this.getBaselineNodes(node.value)
        if (baselineNodes.length === 0) {
          nodes.push(
            { value: null, label: '无', leaf: true, disabled: true }
          )
        }
        for (let i = 0; i < baselineNodes.length; i++) {
          nodes.push(
            { value: baselineNodes[i].version, label: baselineNodes[i].name, leaf: true }
          )
        }
      }
      resolve(nodes)
    },
    submitAnalyze () {
      var node = this.$refs.analyzeScopeRef.getCheckedNodes()[0]
      if (!node) return this.$message.error('请选择需求分析范围！')
      var scopeVersion = node.value // 如果version为null，则说明是当前版本
      var scopeProjectId = node.pathNodes[0].value
      if (this.activeAnalyzeIndex === '0') this.conflictAnalyze(scopeProjectId, scopeVersion)
      else if (this.activeAnalyzeIndex === '1') this.similarityAnalyze(scopeProjectId, scopeVersion)
      else if (this.activeAnalyzeIndex === '2') this.relationshipAnalyze(scopeProjectId, scopeVersion)
    },
    // 冲突检测
    async conflictAnalyze (scopeProjectId, scopeVersion) {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/requirement/analyze/conflict',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          scope: {
            project_id: scopeProjectId,
            version: scopeVersion
          },
          target_type: 'tree',
          target_data: this.requirementTree
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.conflictAnalyzeTable = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 共性识别
    async similarityAnalyze (scopeProjectId, scopeVersion) {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/requirement/analyze/similarity',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          scope: {
            project_id: scopeProjectId,
            version: scopeVersion
          },
          target_type: 'tree',
          target_data: this.requirementTree
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.similarityAnalyzeTable = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 关联关系分析
    async relationshipAnalyze (scopeProjectId, scopeVersion) {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/requirement/analyze/relationship',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          scope: {
            project_id: scopeProjectId,
            version: scopeVersion
          },
          target_type: 'tree',
          target_data: this.requirementTree
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.relationshipAnalyzeTable = res.data
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
