<template>
  <div>
    <!-- 主体区 -->
    <!-- 主体 -->
    <el-tabs v-model="activeIndex" tab-position="top" style="overflow: auto;">
      <!-- 主要信息 -->
      <el-tab-pane label="主要信息" name="0">
        <el-form label-width="60px" :model="requirementMainForm" :rules="requirementMainFormRules"
        ref="requirementMainFormRef">
          <el-form-item label="名称" prop="name">
            <el-input v-model="requirementMainForm.name"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="requirementMainForm.description" type="textarea" :rows="10"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="editMain()">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <!-- 基本信息 -->
      <el-tab-pane label="基本信息" name="1">
        <el-form label-width="100px" :model="requirementBasicForm">
          <el-form-item label="状态">
            <el-select v-model="requirementBasicForm.status" placeholder="请选择状态">
              <el-option label="未开始" value="未开始"></el-option>
              <el-option label="进行中" value="进行中"></el-option>
              <el-option label="已结束" value="已结束"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="优先级">
            <el-select v-model="requirementBasicForm.priority" placeholder="请选择优先级">
              <el-option label="高" value="高"></el-option>
              <el-option label="中" value="中"></el-option>
              <el-option label="低" value="低"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="预计开始时间">
            <el-date-picker v-model="requirementBasicForm.expectedStartTime" type="date" placeholder="选择日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="预计结束时间">
            <el-date-picker v-model="requirementBasicForm.expectedEndTime" type="date" placeholder="选择日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="创建者">{{this.requirementBasicForm.author}}</el-form-item>
          <el-form-item label="创建时间">{{this.requirementBasicForm.createdTime}}</el-form-item>
          <el-form-item label="最后修改时间">{{this.requirementBasicForm.lastModifyTime}}</el-form-item>
          <el-form-item>
            <el-button type="primary" @click="editBasic()">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <!-- 需求追踪 -->
      <el-tab-pane label="需求追踪" name="2">
        <el-form label-width="80px" :model="requirementTrackForm">
          <el-form-item label="追踪代码">
            <el-input v-model="requirementTrackForm.trackCode" placeholder="追踪到的代码"></el-input>
          </el-form-item>
          <el-form-item label="追踪测试">
            <el-input v-model="requirementTrackForm.trackTest" placeholder="追踪到的测试用例"></el-input>
          </el-form-item>
          <el-form-item label="追踪人员">
            <el-input v-model="requirementTrackForm.trackPeople" placeholder="追踪到的开发人员"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="editTrack()">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <!-- 需求分析 -->
      <el-tab-pane label="需求分析" name="3">
        <!-- 范围选择区 -->
        <el-cascader :props="analyzeScopeProps" style="margin-left: 10px; margin-bottom: 20px;"
        placeholder="请选择需求分析范围" ref="analyzeScopeRef"></el-cascader>
        <el-button type="success" size="medium" style="margin-left: 10px;"
        @click="submitAnalyze">开始分析</el-button>
        <el-tabs v-model="activeAnalyzeIndex" type="card">
          <el-tab-pane label="冲突检测" name="0">
            <el-table :data="conflictAnalyzeTable">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" class="analyze-table-form">
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req0.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req0.description }}</span>
                    </el-form-item>
                    <el-divider></el-divider>
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req1.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req1.description }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column label="需求条目一" prop="req0.name"></el-table-column>
              <el-table-column label="需求条目二" prop="req1.name"></el-table-column>
              <el-table-column label="冲突类型" prop="_type">
                <template slot-scope="props"><el-tag type="danger">{{ props.row._type }}</el-tag></template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="共性识别" name="1">
            <el-table :data="similarityAnalyzeTable">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" class="analyze-table-form">
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req0.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req0.description }}</span>
                    </el-form-item>
                    <el-divider></el-divider>
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req1.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req1.description }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column label="需求条目一" prop="req0.name"></el-table-column>
              <el-table-column label="需求条目二" prop="req1.name"></el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="关联关系" name="2">
            <el-table :data="relationshipAnalyzeTable">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" class="analyze-table-form">
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req0.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req0.description }}</span>
                    </el-form-item>
                    <el-divider></el-divider>
                    <el-form-item label="需求名称">
                      <span>{{ props.row.req1.name }}</span>
                    </el-form-item>
                    <el-form-item label="需求描述">
                      <span>{{ props.row.req1.description }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column label="需求条目一" prop="req0.name"></el-table-column>
              <el-table-column label="需求条目二" prop="req1.name"></el-table-column>
              <el-table-column label="关联关系类型" prop="_type">
                <template slot-scope="props"><el-tag type="success">{{ props.row._type }}</el-tag></template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  created () {
    this.getRequirementProfile()
  },
  data () {
    return {
      projectsName: 'MyProject',
      activeIndex: '0',
      activeAnalyzeIndex: '0',
      requirementMainForm: {
        name: '',
        description: ''
      },
      requirementBasicForm: {
        _type: '',
        status: '',
        priority: '',
        expectedStartTime: '',
        expectedEndTime: '',
        author: '',
        createdTime: '',
        lastModifyTime: ''
      },
      requirementTrackForm: {
        trackCode: '',
        trackTest: '',
        trackPeople: ''
      },
      requirementMainFormRules: {
        name: [
          { required: true, message: '请输入需求条目名称', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入需求条目描述', trigger: 'blur' }
        ]
      },
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
    // 获取需求信息
    async getRequirementProfile () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/requirement/profile',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          requirement_id: this.$route.query.requirementId
        }
      })
      if (res.meta.status === 200) {
        // 给表单赋值
        this.requirementMainForm.name = res.data.name
        this.requirementMainForm.description = res.data.description
        this.requirementBasicForm._type = res.data._type
        this.requirementBasicForm.status = res.data.status
        this.requirementBasicForm.priority = res.data.priority
        this.requirementBasicForm.expectedStartTime = res.data.expected_start_time
        this.requirementBasicForm.expectedEndTime = res.data.expected_end_time
        this.requirementBasicForm.author = res.data.author
        this.requirementBasicForm.createdTime = res.data.created_time
        this.requirementBasicForm.lastModifyTime = res.data.last_modify_time
        this.requirementTrackForm.trackCode = res.data.track_code
        this.requirementTrackForm.trackTest = res.data.track_test
        this.requirementTrackForm.trackPeople = res.data.track_people
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 修改主要信息
    async editMain () {
      // 校验
      this.$refs.requirementMainFormRef.validate(async valid => {
        if (!valid) return
        // 弹框
        this.$messageBox('在保存修改内容前是否需要进行需求分析？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '前往需求分析',
          cancelButtonText: '保存'
        }).then(() => {
          this.activeIndex = '3'
        }).catch(async action => {
          if (action === 'cancel') {
            const { data: res } = await this.$http({
              method: 'put',
              url: '/requirement/edit',
              headers: {
                'Authorization': window.sessionStorage.getItem('token')
              },
              data: {
                requirement_id: this.$route.query.requirementId,
                name: this.requirementMainForm.name,
                description: this.requirementMainForm.description
              }
            })
            if (res.meta.status === 200) {
              this.$message.success(res.meta.msg)
              this.getRequirementProfile()
              this.activeIndex = '2'
            } else {
              this.$message.error(res.meta.msg)
            }
          } else {
            this.$message({ type: 'info', message: '操作已取消' })
          }
        })
      })
    },
    // 修改基本信息
    async editBasic () {
      const { data: res } = await this.$http({
        method: 'put',
        url: '/requirement/edit',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          requirement_id: this.$route.query.requirementId,
          status: this.requirementBasicForm.status,
          priority: this.requirementBasicForm.priority,
          expected_start_time: this.requirementBasicForm.expectedStartTime,
          expected_end_time: this.requirementBasicForm.expectedEndTime
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.getRequirementProfile()
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 修改需求追踪
    async editTrack () {
      const { data: res } = await this.$http({
        method: 'put',
        url: '/requirement/edit',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          requirement_id: this.$route.query.requirementId,
          track_code: this.requirementTrackForm.trackCode,
          track_test: this.requirementTrackForm.trackTest,
          track_people: this.requirementTrackForm.trackPeople
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.getRequirementProfile()
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
          target_type: 'edit_single',
          target_data: {
            _id: this.$route.query.requirementId,
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            _type: this.requirementBasicForm._type
          }
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
          target_type: 'edit_single',
          target_data: {
            _id: this.$route.query.requirementId,
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            _type: this.requirementBasicForm._type
          }
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
          target_type: 'edit_single',
          target_data: {
            _id: this.$route.query.requirementId,
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            _type: this.requirementBasicForm._type
          }
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
