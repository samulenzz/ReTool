<template>
  <div>
    <!-- 面包屑区域 -->
    <div>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        <el-breadcrumb-item :to="{
          path: '/projects/projectHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.projectForm.projectName
          }
        }">{{projectForm.projectName}}</el-breadcrumb-item>
        <el-breadcrumb-item>项目信息</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体区 -->
    <el-card class="box-card">
      <!-- 主体 -->
      <el-tabs v-model="activeIndex" tab-position="left" style="overflow: auto;">
        <!-- 项目信息 -->
        <el-tab-pane label="项目信息" name="0">
          <el-form class="project-form" label-position="top" label-width="100px" :model="projectForm"
            ref="projectFormRef" :rules="projectFormRules">
            <el-form-item label="项目名称" prop="projectName">
              <el-input v-model="projectForm.projectName"></el-input>
            </el-form-item>
            <el-form-item label="详细描述">
              <el-input v-model="projectForm.description" type="textarea" :rows="3"></el-input>
            </el-form-item>
            <el-form-item label="项目状态">
              <el-select v-model="projectForm.status" placeholder="请选择项目状态">
                <el-option label="未开始" value="未开始"></el-option>
                <el-option label="进行中" value="进行中"></el-option>
                <el-option label="已结束" value="已结束"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="editProjectProfile()">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 成员管理 -->
        <el-tab-pane label="成员管理" name="1">
          <!-- 顶部区域 -->
          <el-row :gutter="10">
            <el-col :span="4">
              <el-select v-model="newProjectUser" filterable placeholder="请输入用户名">
                <el-option v-for="user in userList" :key="user.username" :label="user.username" :value="user.username">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="1">
              <el-button type="primary" @click="addUser()">添加用户</el-button>
            </el-col>
          </el-row>
          <!-- 用户表格区 -->
          <el-table ref="projectUsersRef" :data="projectUsers">
            <el-table-column type="index"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="projectRole" label="项目角色"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-tooltip effect="light" content="修改项目角色" placement="top-start">
                  <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEditProjectRole(scope.row.username)"></el-button>
                </el-tooltip>
                <el-tooltip effect="light" content="删除用户" placement="top-start">
                  <el-button type="danger" size="small" icon="el-icon-delete" @click="deleteUser(scope.row.username)"></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <!-- 确认按钮区 -->
          <el-button type="primary" @click="submitEditProjectUser()" style="margin-top: 20px;">保存</el-button>
        </el-tab-pane>

        <!-- 基线管理 -->
        <el-tab-pane label="基线管理" name="2">
          <!-- 工具栏 -->
          <el-row :gutter="20" style="margin-bottom: 20px;">
            <el-col :span="4">
              <el-button type="primary" size="small" @click="handleAddBaselineNode()">创建基线节点</el-button>
            </el-col>
          </el-row>
          <el-timeline reverse>
            <el-timeline-item v-for="node in baselineNodes" :key="node.version"
            :timestamp="node.created_time" placement="top">
             <!-- click的用法参考 https://www.jianshu.com/p/39553cc705ea -->
              <el-card shadow="hover" @click.native="jumpToArchiveRequirementHomepage(node.version)">
                <h4>{{node.name}}</h4>
                <p>{{node.description}}</p>
                <p style="color: #5c3317; font-size: small;">{{node.author}} 创建于 {{node.created_time}}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- Dialog区 -->
    <!-- 修改角色 -->
    <el-dialog title="修改角色" :visible.sync="dialogVisiable.editProjectRole" width="30%">
      <el-form label-position="right" label-width="80px" :model="editProjectRoleForm"
        :rules="editProjectRoleFormRules" ref="editProjectRoleFormRef">
        <el-form-item label="用户名">
          <el-input v-model="editProjectRoleForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="项目角色" prop="projectRole">
          <el-select v-model="editProjectRoleForm.projectRole" placeholder="请选择项目角色">
            <el-option label="项目经理" value="项目经理"></el-option>
            <el-option label="项目组长" value="项目组长"></el-option>
            <el-option label="普通成员" value="普通成员"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisiable.editProjectRole = false">取 消</el-button>
        <el-button type="primary" @click="editProjectRole()">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 添加归档版本节点 -->
    <el-dialog title="创建基线节点" :visible.sync="dialogVisiable.addBaselineNode" width="30%">
      <el-form label-position="right" label-width="80px" :model="addBaselineNodeForm"
      :rules="addBaselineNodeFormRules" ref="addBaselineNodeFormRef">
      <el-form-item label="版本名称" prop="name">
        <el-input v-model="addBaselineNodeForm.name" placeholder="请输入版本名称，例如v0.1.0"></el-input>
      </el-form-item>
      <el-form-item label="版本描述" prop="description">
        <el-input v-model="addBaselineNodeForm.description" placeholder="请输入版本描述"
         type="textarea" :rows="3"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisiable.addBaselineNode = false">取 消</el-button>
      <el-button type="primary" @click="addBaselineNode()">确 定</el-button>
    </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  created () {
    this.getProjectProfile()
    this.getProjectUserList()
    this.getUserList()
    this.getBaselineNodes()
  },
  data () {
    return {
      activeIndex: '0',
      dialogVisiable: {
        editProjectRole: false,
        addBaselineNode: false
      },
      projectForm: {
        projectName: '',
        description: '',
        status: ''
      },
      projectFormRules: {
        projectName: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      },
      // 系统中的所有用户
      userList: [],
      // 查询框中新添加的用户
      newProjectUser: '',
      // 修改用户角色表单
      editProjectRoleForm: {
        username: '',
        projectRole: ''
      },
      editProjectRoleFormRules: {
        projectRole: { required: true, message: '请选择角色', trigger: 'change' }
      },
      // 项目内的用户
      projectUsers: [],
      // 基准线节点
      baselineNodes: [],
      addBaselineNodeForm: {
        name: '',
        description: ''
      },
      addBaselineNodeFormRules: {
        name: [
          { required: true, message: '请输入归档版本名称', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 获取用户列表
    async getUserList () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/user/list_all',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        }
      })
      if (res.meta.status === 200) {
        this.userList = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 获取项目信息
    async getProjectProfile () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/project/profile',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: this.$route.query.projectId
        }
      })
      if (res.meta.status === 200) {
        this.projectForm.projectName = res.data.project_name
        this.projectForm.description = res.data.description
        this.projectForm.status = res.data.status
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 获取项目用户
    async getProjectUserList () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/project/user/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: this.$route.query.projectId
        }
      })
      if (res.meta.status === 200) {
        // 将用户存入projectUsers中
        for (let i = 0; i < res.data.length; i++) {
          this.projectUsers.push({
            username: res.data[i].username,
            projectRole: res.data[i].project_role
          })
        }
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 修改项目信息
    async editProjectProfile () {
      this.$refs.projectFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$http({
          method: 'put',
          url: '/project/edit',
          headers: {
            'Authorization': window.sessionStorage.getItem('token')
          },
          data: {
            project_id: this.$route.query.projectId,
            project_name: this.projectForm.projectName,
            description: this.projectForm.description,
            status: this.projectForm.status
          }
        })
        if (res.meta.status === 200) {
          this.$message.success(res.meta.msg)
        } else {
          this.$message.error(res.meta.msg)
        }
      })
    },
    addUser () {
      // 检查是否为空
      if (this.newProjectUser === '') return
      // 检查该用户是否已经存在
      for (let i = 0; i < this.projectUsers.length; i++) {
        if (this.projectUsers[i].username === this.newProjectUser) {
          this.$message.error('该用户已存在！')
          return
        }
      }
      this.projectUsers.push({
        username: this.newProjectUser,
        projectRole: '普通成员'
      })
    },
    handleEditProjectRole (username) {
      this.editProjectRoleForm.username = username
      this.dialogVisiable.editProjectRole = true
    },
    editProjectRole () {
      this.$refs.editProjectRoleFormRef.validate(async valid => {
        if (!valid) return
        for (let i = 0; i < this.projectUsers.length; i++) {
          if (this.projectUsers[i].username === this.editProjectRoleForm.username) {
            this.projectUsers[i].projectRole = this.editProjectRoleForm.projectRole
            this.dialogVisiable.editProjectRole = false
            break
          }
        }
      })
    },
    deleteUser (username) {
      for (var i = 0; i < this.projectUsers.length; i++) {
        if (this.projectUsers[i].username === username) {
          break
        }
      }
      this.projectUsers.splice(i, 1)
    },
    async submitEditProjectUser () {
      // 准备users
      var users = []
      for (let i = 0; i < this.projectUsers.length; i++) {
        users.push({
          username: this.projectUsers[i].username,
          project_role: this.projectUsers[i].projectRole
        })
      }
      const { data: res } = await this.$http({
        method: 'put',
        url: '/project/user/edit',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          project_id: this.$route.query.projectId,
          users: users
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    handleAddBaselineNode () {
      this.dialogVisiable.addBaselineNode = true
    },
    // 获取基线节点列表
    async getBaselineNodes () {
      const { data: res } = await this.$http({
        method: 'get',
        url: '/project/baseline/node/list',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        params: {
          project_id: this.$route.query.projectId
        }
      })
      if (res.meta.status === 200) {
        this.baselineNodes = res.data
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 增加归档版本节点
    async addBaselineNode () {
      const { data: res } = await this.$http({
        method: 'post',
        url: '/project/baseline/node/create',
        headers: {
          'Authorization': window.sessionStorage.getItem('token')
        },
        data: {
          name: this.addBaselineNodeForm.name,
          description: this.addBaselineNodeForm.description,
          project_id: this.$route.query.projectId
        }
      })
      if (res.meta.status === 200) {
        this.$message.success(res.meta.msg)
        this.dialogVisiable.addBaselineNode = false
        this.getBaselineNodes()
      } else {
        this.$message.error(res.meta.msg)
      }
    },
    // 跳转到归档需求主页
    jumpToArchiveRequirementHomepage (version) {
      this.$router.push(
        {
          path: '/projects/archive/projectHomepage',
          query: {
            projectId: this.$route.query.projectId,
            projectName: this.projectForm.projectName,
            version: version
          }
        }
      )
    }
  }
}
</script>

<style lang="less" scoped>
.project-form {
  width: 800px;
}
</style>
