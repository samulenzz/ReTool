<template>
  <div class="main-container">
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{
          path: '/projects/projectHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.$route.query.projectName
          }
        }">{{this.$route.query.projectName}}</el-breadcrumb-item>
        <el-breadcrumb-item>创建单条需求条目</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 头部步骤条区 -->
      <el-alert title="创建单条需求条目" type="info" center show-icon></el-alert>
      <el-steps :active="activeIndex - 0" align-center>
        <el-step title="主要信息"></el-step>
        <el-step title="基本信息"></el-step>
        <el-step title="需求分析"></el-step>
      </el-steps>
      <!-- 主体 -->
      <el-tabs v-model="activeIndex" tab-position="left" style="overflow: auto;"
      :before-leave="beforeTabLeave">
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
              <el-button type="primary" @click="nextstep()" style="margin-top: 20px;">下一步</el-button>
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
              <el-date-picker v-model="requirementBasicForm.expectedStartTime" type="date" placeholder="选择日期" :picker-options="startTime1">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="预计结束时间">
              <el-date-picker v-model="requirementBasicForm.expectedEndTime" type="date" placeholder="选择日期" :picker-options="endTime1">
              </el-date-picker>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="nextstep()" style="margin-top: 20px;">下一步</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <!-- 需求分析 -->
        <el-tab-pane label="需求分析" name="2">
          <!-- 范围选择区 -->
          <el-cascader :props="analyzeScopeProps" style="margin-left: 10px; margin-bottom: 20px;"
          placeholder="请选择需求分析范围" ref="analyzeScopeRef"></el-cascader>
          <el-button type="success" size="medium" style="margin-left: 10px;"
          @click="submitAnalyze">开始分析</el-button>
          <el-tabs v-model="activeAnalyzeIndex" type="card" style="margin-left: 10px;">
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
          <el-button type="primary" @click="addRequirement()"
          style="margin-top: 20px; margin-left: 10px;">创建</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      projectsName: 'My projects',
      activeIndex: '0',
      activeAnalyzeIndex: '0',
      // 是否允许切换Tab
      isAllowTabLeave: false,
      requirementMainForm: {
        name: '',
        description: ''
      },
      requirementBasicForm: {
        status: '',
        priority: '',
        expectedStartTime: '',
        expectedEndTime: ''
      },
      startTime1: {
        disabledDate: time => {
          // 如果已经已知结束日期，就把结束日期之后的日期禁用
          if (this.requirementBasicForm.expectedEndTime) {
            return (
              time.getTime() > new Date(this.requirementBasicForm.expectedEndTime).getTime()
            )
          } else { // 否则 就把当前日期之前的日期禁用掉
            return time.getTime() <= Date.now()
          }
        }
      },
      endTime1: {
        disabledDate: time => {
          // 如果已知开始日期，就把开始日期之前的日期禁用掉
          if (this.requirementBasicForm.expectedStartTime) {
            return (
              time.getTime() < new Date(this.requirementBasicForm.expectedStartTime).getTime()
            )
          }
        }
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
    // 检测需求是否被填写完成
    beforeTabLeave (newActive, oldActive) {
      if (oldActive === '0' && newActive !== '0') {
        this.$refs.requirementMainFormRef.validate(valid => {
          if (!valid) {
            this.$message.error('请完成基本信息！')
            this.isAllowTabLeave = false
          } else {
            this.isAllowTabLeave = true
          }
        })
      }
      return this.isAllowTabLeave
    },
    // 点击下一步
    nextstep () {
      this.beforeTabLeave('1', '0')
      if (this.isAllowTabLeave === true) {
        if (this.activeIndex === '0') {
          this.activeIndex = '1'
        } else if (this.activeIndex === '1') {
          this.activeIndex = '2'
        }
      }
    },
    async addRequirement () {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/requirement/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          project_id: this.$route.query.projectId,
          base_id: this.$route.query.baseId,
          location: this.$route.query.location,
          name: this.requirementMainForm.name,
          description: this.requirementMainForm.description,
          status: this.requirementBasicForm.status,
          priority: this.requirementBasicForm.priority,
          expected_start_time: this.requirementBasicForm.expectedStartTime,
          expected_end_time: this.requirementBasicForm.expectedEndTime
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.$router.push({
          path: '/requirements/requirementHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.$route.query.projectName,
            requirementId: res.data.requirement_id
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
    // 获取基线节点
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
          target_type: 'add_single',
          target_data: {
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            base_id: this.$route.query.baseId,
            project_id: this.$route.query.projectId
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
          target_type: 'add_single',
          target_data: {
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            base_id: this.$route.query.baseId,
            project_id: this.$route.query.projectId
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
          target_type: 'add_single',
          target_data: {
            name: this.requirementMainForm.name,
            description: this.requirementMainForm.description,
            base_id: this.$route.query.baseId,
            project_id: this.$route.query.projectId
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
.main-container {
  height: 100%;
}

.el-form {
  width: 70%;
}

.el-tabs__content {
  margin-left: 100px;
}
</style>

<style lang="less">
/* 必须设置成全局，去掉scoped */
/* 参考：https://segmentfault.com/q/1010000017251094 */
.analyze-table-form label {
  color: #99a9bf
}
</style>
