<template>
  <div>
    <!-- 主体区 -->
    <!-- 主体 -->
    <el-tabs v-model="activeIndex" tab-position="top" style="overflow: auto;">
      <!-- 主要信息 -->
      <el-tab-pane label="主要信息" name="0">
        <el-form label-width="60px" :model="requirementMainForm">
          <el-form-item label="名称">
            <el-input v-model="requirementMainForm.name"></el-input>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="requirementMainForm.description" type="textarea" :rows="10"></el-input>
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
        </el-form>
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
      requirementMainForm: {
        name: '',
        description: ''
      },
      requirementBasicForm: {
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
      }
    }
  },
  methods: {
    // 获取需求信息
    async getRequirementProfile () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/requirement/archive/profile',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          requirement_id: this.$route.query.requirementId,
          version: this.$route.query.version
        }
      })
      if (res.meta.status === 200) {
        // 给表单赋值
        this.requirementMainForm.name = res.data.name
        this.requirementMainForm.description = res.data.description
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
    }
  }
}
</script>

<style lang="less" scoped>
.el-form {
  width: 70%;
}
</style>
