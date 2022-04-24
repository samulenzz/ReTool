<template>
  <div id="app">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模板管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/templates/templateList' }">模板列表</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/templates/documentList' }">文档管理</el-breadcrumb-item>
        <el-breadcrumb-item>{{ chosenDocument.document_name }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 主体区域 -->
    <el-card class="box-card">
      <!-- v-model="" -->
      <el-tabs tab-position="top" style="overflow: auto;">
        <!-- 文档基本信息编辑区域 -->
        <el-tab-pane label="需求文档基本信息编辑" name="0" v-loading="loadingTag.info">
          <el-form v-bind:model="chosenDocument" label-width="auto">
            <el-form-item label="文档名称">
              <el-col :span="11">
                <el-input v-model="chosenDocument.document_name"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="所属模板">
              <el-col :span="11">
                <el-input v-model="chosenDocument.template_name" :disabled="true"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="文档简介">
              <el-col :span="11">
                <el-input type="textarea" v-model="chosenDocument.introduction" :autosize="{minRows: 6,maxRows: 20}"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="最后修改时间">
              <el-col :span="11">
                <el-input v-model="chosenDocument.last_time" :disabled="true"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="用户反馈数据集列表">
              <div v-if="chosenDocument.comments_file_list.length <= 0">暂无数据</div>
              <el-tag v-for="(fileName, i) in chosenDocument.comments_file_list" :key="(fileName, i)" closable @close="deleteCommentsFile(fileName, i)">{{fileName}}</el-tag>
              <el-upload :limit="1" :auto-upload="true" action="" :multiple="false" accept=".csv" :http-request="addCommentsFile">
                <el-button slot="trigger" size="small" type="success">
                  选取文件<i class="el-icon-document"></i>
                </el-button>
                <el-button type="warnig" style="margin-left: 10px;" size="small" @click="submitCommentsFile()">
                  用户反馈上传<i class="el-icon-upload"></i>
                </el-button>
                <div slot="tip" class="el-upload__tip" style="line-height: 10px;">只能上传csv文件，且不超过500kb</div>
              </el-upload>
            </el-form-item>
            <el-form-item label="">
              <el-button type="primary" @click="editDocument()">提交更改</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <!-- 用户反馈分析区域 -->
        <el-tab-pane label="用户反馈管理和分析" name="1" v-loading="loadingTag.info">
          <!-- 用户反馈文件下拉列表 -->
          <!-- 选择一个用户反馈 -->
          <el-row :gutter="20">
            <el-col :span="5">
              <el-select v-model="comments_file_name" clearable filterable placeholder="请选择一个用户反馈数据集">
                <el-option
                 v-for="comments in chosenDocument.comments_file_list"
                 :key="comments"
                 :label="comments"
                 :value="comments">
                </el-option>
              </el-select>
            </el-col>
            <!-- 用户反馈上传按钮 -->
            <el-col :span="5">
              <el-upload :limit="1" :auto-upload="true" action="" :multiple="false" accept=".csv" :http-request="addCommentsFile">
                <el-button slot="trigger" size="small" type="primary">
                  选取文件<i class="el-icon-document"></i>
                </el-button>
                <el-button type="success" style="margin-left: 10px;" size="small" @click="submitCommentsFile()">
                  用户反馈上传<i class="el-icon-upload"></i>
                </el-button>
                <div slot="tip" class="el-upload__tip">只能上传csv文件，且不超过500kb</div>
              </el-upload>
            </el-col>
            <!-- 用户反馈分类 -->
            <el-col :span="6">
              <el-button type="primary" size="small" @click="doClassification()">
                用户反馈分类<i class="el-icon-s-marketing"></i>
              </el-button>
            <!-- 用户反馈词云按钮 -->
              <el-button type="warning" style="margin-left: 10px;" size="small" @click="getWordCloud()">
                生成词云<i class="el-icon-picture"></i>
              </el-button>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-bottom: 20px;">
            <!-- 词云 -->
            <el-card class="inner-box-card" shadow="hover">
              <div slot="header">
                <span style="color: black;">用户反馈词云</span>
              </div>
              <div v-if="this.wordcloud_img.length > 0">
                <el-tooltip effect="dark" :content="'所属数据集为：'+this.comments_file_name" placement="top-start">
                  <div style="position:relative;left:33%;width:38%;"><el-image :src="this.wordcloud_img"></el-image></div>
                </el-tooltip>
              </div>
            </el-card>
            <!-- 用户反馈分类 -->
            <el-card class="inner-box-card" shadow="hover" v-loading='loadingTag.classify'>
              <div slot="header">
                <span style="color: black;">用户反馈分类结果</span>
              </div>
              <!-- 表格 -->
              <!-- 两个下拉选择框，选择aspect和label显示在表格中 -->
              <el-form label-width="auto" v-if="classifyResultTable != null">
                <el-form-item v-if="classifyResultTable != null" label="需求类别">
                  <el-select v-model="classifyAspect" clearable filterable placeholder="请选择">
                    <el-option v-for="aspect in Object.keys(classifyResultTable)"
                      :key="aspect"
                      :label="aspect"
                      :value="aspect">
                    </el-option>
                  </el-select>
                  <el-select v-model="classifyLabel" clearable filterable placeholder="请选择"
                    v-if="classifyResultTable != null && classifyAspect.length != 0" style="margin-left: 10px;">
                    <el-option v-for="label in Object.keys(classifyResultTable[classifyAspect])"
                      :key="label"
                      :label="label"
                      :value="label"
                      :disabled="classifyResultTable[classifyAspect][label].length == 0">
                    </el-option>
                  </el-select>
                  <!-- 相似性分析某些需求 -->
                  <el-tooltip effect="light" content="分析相似性" placement="top-start">
                    <el-button size="medium" type="danger" @click="analyzeSimilarity()" style="margin-left: 10px;">
                      相似性分析<i class="el-icon-data-analysis"></i>
                    </el-button>
                  </el-tooltip>
                </el-form-item>
              </el-form>
              <!-- 或者两行复选框，至多展示五个表格 -->
              <!-- <el-checkbox-group :min="1" :max="1" v-model="classifyAspect" v-if="classifyResultTable != null">
                <el-checkbox v-for="aspect in Object.keys(classifyResultTable)" :key="aspect" :label="aspect"></el-checkbox>
              </el-checkbox-group> -->
              <el-table v-if="classifyResultTable != null && classifyAspect.length != 0 && classifyLabel.length != 0"
                :data="classifyResultTable[classifyAspect][classifyLabel]"
                default-expand-all border
                row-key="comment"
                :tree-props="{children: 'children'}"
                :row-class-name="getTableRowClassName"
                height="400">
                <el-table-column type="index" label="#"></el-table-column>
                <el-table-column label="用户评论">
                  <template slot-scope="scope">
                    <span>{{scope.row.comment}}</span>
                  </template>
                </el-table-column>
                <!-- <el-table-column prop="problem" label="test"></el-table-column> -->
              </el-table>
            </el-card>
          </el-row>
        </el-tab-pane>
        <!-- 文档内容编辑 -->
        <el-tab-pane label="文档内容编辑" name="2" v-loading="loadingTag.info">
          <el-row :gutter="20" style="margin-bottom: 20px;">
            <el-col :span="6">
              <div><span style="color: black;">目录</span></div>
            </el-col>
            <el-col :span="18"></el-col>
          </el-row>
          <el-row :gutter="20">
            <!-- 文档目录区 -->
            <el-col :span="6">
              <div :key="(line, i)" v-for="(line, i) in chosenDocument.outline">
                <el-tag closable
                 @click="outlintIndex = i" effect="plain" @close="deleteOutline(line, i)">
                {{ line }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="12">
              <el-form label-width="auto" v-if="outlintIndex >= 0">
                <el-form-item label="大纲">
                  <el-input v-model="chosenDocument.outline[outlintIndex]"></el-input>
                </el-form-item>
                <el-form-item label="内容">
                  <el-input v-model="chosenDocument.contents[outlintIndex]" type="textarea" :autosize="{minRows: 8,maxRows: 20}"></el-input>
                </el-form-item>
                <el-form-item label="">
                  <el-button type="primary" @click="editDocument()">提交更改</el-button>
                </el-form-item>
              </el-form>
            </el-col>
            <!-- 需求表格区 -->
            <!-- <el-col :span="18"> -->
              <!-- 加key是为了刷新子页面 -->
              <!-- https://segmentfault.com/q/1010000015992883 -->
              <!-- https://blog.csdn.net/u010176097/article/details/81252417 -->
              <!-- <router-view :key="$route.fullPath" @fresh="fresh"></router-view> -->
            <!-- </el-col> -->
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>/* eslint-disable */
// ProjectHomePage.vue
  export default {
    created() {
      this.document_id = this.$route.query.document_id
      this.getDocument()
    },
    data() {
      return {
        // loading tag
        loadingTag: {
          info: false,
          classify: false
        },
        document_id: '',
        chosenDocument: {
          _id: '',
          document_name: '',
          template_name: '',
          introduction: '',
          last_time: "",
          outline: [],
          contents: [],
          comments_file_list: []
        },
        // show outline and content
        outlintIndex: -1,
        // comments chose
        comments_file_name: '',
        // comments upload
        commentsFile: null,
        // wordcloud image base64
        wordcloud_img: '',
        // classify result
        classifyResultTable: null,
        classifyAspect: '',
        classifyLabel: ''
      }
    },
    methods: {
      getDocument: async function() {
        if (this.document_id.length === 0) {
          return this.$message.error('错误！')
        }
        this.loadingTag.info = true
        const {
          data: res
        } = await this.$http({
          method: 'get',
          url: '/document/profile',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          params: {
            document_id: this.document_id
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.chosenDocument = res.data.document
        } else {
          this.$message.error(res.meta.msg)
        }
        this.loadingTag.info = false
        // clear attributes
        this.outlintIndex = -1
        this.comments_file_name = ''
        this.commentsFile = null
        this.wordcloud_img = ''
        this.classifyResultTable = null
        this.classifyAspect = ''
        this.classifyLabel = ''
      },
      editDocument: function() {
        this.$messageBox('确认提交该模板？(该操作不可逆)', {
          type: 'warning'
        }).then(async () => {
          const {
            data: res
          } = await this.$http({
            method: "post",
            url: "/document/edit",
            headers: {
              'Authorization': window.sessionStorage.getItem('token')
            },
            data: {
              document: this.chosenDocument
            }
          })
          if (res.meta.status === 200) {
            this.$message.success(res.meta.msg)
            this.getDocument()
          } else {
            this.$message.error(res.meta.msg)
          }
        }).catch(() => {
          this.$message.info('已取消删除')
        })
      },
      // 删除表格某一行
      deleteRow: function(index, rows) {
        rows.splice(index, 1);
      },
      deleteOutline: function(line, index) {
        this.$messageBox('确认删除\"' + line + '\"', {
          type: 'warning'
        }).then(async () => {
          this.chosenDocument.outline.splice(index, 1)
          this.chosenDocument.contents.splice(index, 1)
          const {
            data: res
          } = await this.$http({
            method: "post",
            url: "/document/edit",
            headers: {
              'Authorization': window.sessionStorage.getItem('token')
            },
            data: {
              document: this.chosenDocument
            }
          })
          if (res.meta.status === 200) {
            this.$message.success(res.meta.msg)
            this.getDocument()
          } else {
            this.$message.error(res.meta.msg)
          }
        }).catch(() => {
          this.$message.info('已取消删除')
        })
      },
      deleteCommentsFile: function(fileName, index) {
        this.$messageBox('确认删除\"' + fileName + '\"', {
          type: 'warning'
        }).then(async () => {
          this.chosenDocument.comments_file_list.splice(index, 1)
          this.editDocument()
        }).catch(() => {
          this.$message.info('已取消')
        })
      },
      addCommentsFile: function(file) {
        this.commentsFile = file.file
      },
      submitCommentsFile: async function() {
        if (!this.commentsFile) {
          return this.$message.error('请选择文件！')
        }
        let formData = new FormData()
        formData.append('document_id', this.document_id)
        formData.append('file', this.commentsFile)
        const {
          data: res
        } = await this.$http({
          method: 'post',
          url: 'document/comments/upload',
          headers: {
            'Authorization': window.sessionStorage.getItem('token'),
            'Content-type': 'multipart/form-data'
          },
          data: formData
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.getDocument()
        } else {
          this.$message.error(res.meta.msg)
        }
      },
      getWordCloud: async function() {
        if (this.comments_file_name.length == 0) {
          return this.$message.error('请选择用户反馈数据集！')
        }
        const {
          data : res
        } = await this.$http({
          method: 'get',
          url: 'document/comments/wordcloud',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          params: {
            document_id: this.document_id,
            comments_file_name: this.comments_file_name
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          // process the base64 img
          let img_base64_str = res.data.img_base64
          // console.log(img_base64_str);
          // data:image/png;base64,
          this.wordcloud_img = 'data:image/png;base64,' + img_base64_str
        } else {
          this.$message.error(res.meta.msg)
        }
      },
      doClassification: async function() {
        if (this.comments_file_name.length == 0) {
          return this.$message.error('请选择用户反馈数据集！')
        }
        this.loadingTag.classify = true
        const {
          data : res
        } = await this.$http({
          method: 'post',
          url: 'document/comments/classify',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            document_id: this.document_id,
            comments_file_name: this.comments_file_name
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.classifyResultTable = res.data.classify_result
          console.log(this.classifyResultTable);
        } else {
          this.$message.error(res.meta.msg)
        }
        this.loadingTag.classify = false
      },
      analyzeSimilarity: async function() {
        if (this.classifyAspect.length === 0 || this.classifyLabel.length === 0) {
          return this.$message.error('请选择需求类别！')
        }
        this.loadingTag.classify = true
        const {
          data: res
        } = await this.$http({
          method: 'post',
          url: 'document/comments/similarity',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            'classify_result': this.classifyResultTable,
            'aspect': this.classifyAspect,
            'label': this.classifyLabel
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
          this.classifyResultTable = res.data.classify_result
          console.log(this.classifyResultTable[this.classifyAspect][this.classifyLabel]);
        } else {
          this.$message.error(res.meta.msg)
        }
        this.loadingTag.classify = false
      },
      getTableRowClassName: function({row, rowIndex}) {
        if (row.problem > 0) {
          let index = (parseInt(row.problem) - 1) % 5 + 1
          return 'row' + index
        }
        return ''
      }
    }
  }
</script>

<style lang="less" scoped>
  .box-card {
     margin-top: 20px;
  }
  .inner-box-card {
    margin-top: 20px;
    margin-left: 10px;
    margin-right: 10px;
  }
</style>
<style>
  .el-table .row1 {
    background: oldlace;
  }

  .el-table .row2 {
    background: #f0f9eb;
  }

  .el-table .row3 {
    background: #CCFFFF;
  }

  .el-table .row4 {
    background: #CCCCCC;
  }

  .el-table .row5 {
    background: #FFCCCC;
  }
</style>
