<template>
  <div id="app">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模板管理</el-breadcrumb-item>
        <el-breadcrumb-item>模板列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <el-card class="box-card" style="margin-top: 15px;">
      <!-- 搜索与添加区域 -->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input placeholder="请输入模板关键字" class="input">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <el-table v-loading='loadingTag' class="templateList-table" :data="tempList" border>
        <!-- <el-table-column type="expand">
          <template>
            <el-button>创建新文档</el-button>
          </template>
        </el-table-column> -->
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="template_name" label="模板名">
        </el-table-column>
        <el-table-column prop="introduction" label="模板简介"></el-table-column>
        <el-table-column prop="last_time" label="最后修改时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip effect="light" content="查看或编辑模板" placement="top-start">
              <el-button type="primary" size="small" icon="el-icon-edit" @click="viewTemplate(scope.$index)"></el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="下载模板文档" placement="top-start">
              <el-button type="info" size="small" icon="el-icon-download" @click="downloadTemplate(scope.row.template_name)"></el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="删除模板" placement="top-start">
              <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteTemplate(scope.row.template_name)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 模板查看与编辑功能区域 -->
    <el-dialog title="查看或编辑模板" width="50%" :visible.sync="editDialogVisible">
      <!-- 嵌套表单 -->
      <el-form v-bind:model="chosenTemplate">
        <el-form-item label="模板名" label-width="15%">
          <el-input v-model="chosenTemplate.template_name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="模板简介" label-width="15%">
          <el-input type="textarea" v-model="chosenTemplate.introduction"></el-input>
        </el-form-item>
        <el-form-item label="修改时间" label-width="15%">
          <el-input v-model="chosenTemplate.last_time" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="模板大纲" label-width="15%">
          <el-input v-for="(item, index) in chosenTemplate.outline" :key="index" v-model="chosenTemplate.outline[index]"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="editTemplate()">提交修改</el-button>
      </span>
    </el-dialog>

    <!-- 模板上传功能区域 -->
    <el-card class="box-card" header="模板上传" style="margin-top: 15px;">
      <!-- 头部提示 -->
      <el-alert title="从文本导入模板" type="info" center show-icon></el-alert>
      <!-- 上传功能主体 -->
      <el-tabs tab-position="left" style="overflow: auto; margin-top: 10px;">
        <el-tab-pane label="上传文件" name="0">
          <el-button style="margin-bottom: 10px;margin-top: 10px;" size="small" type="primary" @click="submitUploadFile()">
            上传至服务器
          </el-button>
          <el-tag v-for="tag in uploadFileTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentUploadFileTag"
            style="margin-left: 10px;">
            {{tag.name}}
          </el-tag>
          <el-upload action="" :multiple="false" :limit="1" drag :http-request="addUploadFile" :auto-upload="true" accept=".docx">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击选取文件</em></div>
            <div slot="tip" class="el-upload__tip">只能上传docx文件</div>
          </el-upload>
        </el-tab-pane>
        <el-tab-pane label="模板信息" name="1">
          <el-form>
            <el-form-item label="模板名称">
              <el-input v-model="new_temp_name" style="width: 60%;" placeholder="请输入模板名称"></el-input>
            </el-form-item>
            <el-form-item label="模板简介">
              <el-input v-model="introduction" type="textarea" :rows="4" placeholder="请输入模板简介" style="width: 60%;"></el-input>
            </el-form-item>
            <el-form-item>
              <div>
                <el-button type="success" size="small" @click="createTemplate()">创建模板</el-button>
                <el-tag v-for="tag in itemizeTags" :key="tag.name" :type="tag.type" v-show="tag.name === currentItemizeTag" style="margin-left: 10px;">
                  {{tag.name}}
                </el-tag>
              </div>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  created () {
    this.getTemplateList();
  },
  data () {
    return {
      tempList: [],
      introduction: '',
      new_temp_name: '',
      // variable about upload and create
      uploadFile: null,
      uploadFileToken: '',
      currentUploadFileTag: '',
      uploadFileTags: [
        { name: '上传中', type: 'primary' },
        { name: '上传成功', type: 'success' },
        { name: '上传失败', type: 'danger' }
      ],
      currentItemizeTag: '',
      itemizeTags: [
        { name: '创建中，请稍后...', type: 'primary' },
        { name: '创建成功', type: 'success' },
        { name: '创建失败', type: 'danger' }
      ],
      // varibale about edit and view
      editDialogVisible: false,
      chosenTemplate: {
        _id: '',
        template_name: '',
        last_time: '',
        introduction: '',
        outline: '',
      },
      // loading
      loadingTag: true,
    }
  },
  methods: {
    // 拉取列表
    getTemplateList: async function () {
      this.loadingTag = true
      const {
        data: res
      } = await this.$http({
        method: 'get',
        url: '/template/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        }
      })
      if (res.meta.status === 200) {
        this.tempList = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
      this.loadingTag = false
    },
    deleteTemplate: function(template_name) {
      this.$messageBox('此操作将永久删除该模板, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(
        async () => {
          const {
            data: res
          } = await this.$http({
            method: 'delete',
            url: '/template/delete',
            headers: {
              'Authorization': window.sessionStorage.getItem('token')
            },
            data: {
              template_name: template_name
            }
          })
          if (res.meta.status === 200) {
            this.$message.success(res.meta.msg)
            this.getTemplateList()
          } else {
            this.$message.error(res.meta.msg)
          }
        }
      ).catch(() => {
        this.$message.info('已取消删除')
      })
      // console.log("remove template " + template)
    },
    // 添加文件
    addUploadFile: function(file) {
      this.uploadFile = file.file
      this.currentUploadFileTag = ''
    },
    // // 移除文件
    // removeUploadFile: function(file) {
    //   this.uploadFile = null
    //   this.currentUploadFileTag = ''
    // },
    // 上传模板
    submitUploadFile: async function() {
      if (!this.uploadFile) {
        return this.$message.error('请导入文件！')
      }
      let formData = new FormData()
      formData.append('file', this.uploadFile)
      this.currentUploadFileTag = '上传中'
      const {
        data: res
      } = await this.$http({
        method: 'post',
        url: '/template/upload',
        headers: {
          'Authorization': window.sessionStorage.getItem('token'),
          'Content-type': 'multipart/form-data'
        },
        data: formData
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.currentUploadFileTag = '上传成功'
        this.uploadFileToken = res.data.token
        console.log(this.uploadFileToken)
      } else {
        this.$message.error(res.meta.msg)
        this.currentUploadFileTag = '上传失败'
      }
    },
    // 创建模板
    createTemplate: async function() {
      if (!this.uploadFileToken) {
        return this.$message.error('请先上传文件！')
      }
      this.currentItemizeTag = '创建模板中，请稍后...'
      const {
        data: res
      } = await this.$http({
        method: 'post',
        url: '/template/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          token: this.uploadFileToken,
          introduction: this.introduction
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.currentItemizeTag = '创建模板成功'
        console.log(this.introduction)
        this.introduction = ''
        this.getTemplateList()
      } else {
        this.$message.error(res.meta.msg)
        this.currentItemizeTag = '创建模板失败'
      }
    },
    // 查看模板
    viewTemplate: function (index) {
      this.editDialogVisible = true
      this.chosenTemplate = JSON.parse(JSON.stringify(this.tempList[index]))
      // this.chosenTemplate = this.tempList[index]
      // console.log(this.chosenTemplate.template_name)
    },
    // 编辑模板
    editTemplate: async function () {
      this.$messageBox('确认提交该模板？(该操作不可逆)', {
        type: 'warning'
      }).then(async () => {
          const {
            data: res
          } = await this.$http({
            method: 'put',
            url: '/template/edit',
            headers: {
              'Authorization': window.sessionStorage.getItem('token')
            },
            data: this.chosenTemplate
          })
          if (res.meta.status === 200) {
            this.$message.success(res.meta.msg)
            this.getTemplateList()
          } else {
            this.$message.error(res.meta.msg)
          }
          this.editDialogVisible = false
        })
        .catch(() => {})
    },
    // 下载模板文档
    downloadTemplate: async function(file) {
      console.log("开始下载" + file);
      const {
        data: res
      } = await this.$http({
        method: 'get',
        url: '/template/download',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          // token: this.uploadFileToken,
          // introduction: this.introduction
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .templateList-table {
    margin-top: 15px;
  }
</style>
