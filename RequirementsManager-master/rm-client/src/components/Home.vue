<template>
  <el-container>
    <!-- 侧边栏 -->
    <el-aside width="212px">
      <!-- 头像区 -->
      <div class="user-icon">
        <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png">
      </div>
      <!-- 下拉菜单 -->
      <el-dropdown trigger="click" @command="dropdownHandler">
        <span class="el-dropdown-link">
          {{username}}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="profile">个人信息</el-dropdown-item>
          <el-dropdown-item command="modifyPassword">修改密码</el-dropdown-item>
          <el-dropdown-item command="logout" divided>退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <!-- 分割线 -->
      <hr align=center width=210px color=#fff SIZE=1 />
      <!-- 侧边栏菜单区 -->
      <el-menu background-color="#2d3947" text-color="#fff" active-text-color="#409bff" unique-opened
       router :default-active="navStatus">
        <!-- 用户管理一级菜单 -->
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-user-solid"></i>
            <span>用户管理</span>
          </template>
          <!-- 二级菜单 -->
          <el-menu-item index="/users/userList" @click="saveNavStatus('/users/userList')">
            <template>
              <i class="el-icon-menu"></i>
              <span>用户列表</span>
            </template>
          </el-menu-item>
        </el-submenu>
        <!-- 项目管理一级菜单 -->
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-files"></i>
            <span>项目管理</span>
          </template>
          <!-- 二级菜单 -->
          <el-menu-item index="/projects/projectList"  @click="saveNavStatus('/projects/projectList')">
            <template>
              <i class="el-icon-menu"></i>
              <span>项目列表</span>
            </template>
          </el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>
    <!-- 主体区 -->
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script>
export default {
  created () {
    this.username = window.sessionStorage.getItem('username')
    this.navStatus = window.sessionStorage.getItem('navStatus')
  },
  data () {
    return {
      username: '',
      navStatus: ''
    }
  },
  methods: {
    dropdownHandler (command) {
      if (command === 'logout') {
        window.sessionStorage.clear()
        this.$router.push('/login')
      } else if (command === 'profile') {
        this.$router.push({ path: '/users/profile', query: { username: this.username } })
      } else if (command === 'modifyPassword') {
        this.$router.push({ path: '/users/password', query: { username: this.username } })
      }
    },
    // 保存导航栏状态
    saveNavStatus (status) {
      window.sessionStorage.setItem('navStatus', status)
    }
  }
}
</script>

<style lang="less" scoped>
.el-container {
  height: 100%;
}

.el-aside {
  background-color: #2d3947;

  .user-icon {
    height: 120px;

    img {
      height: 80px;
      width: 80px;
      position: relative;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -40%);
      border-radius: 50%;
    }
  }

  .el-dropdown {
    position: relative;
    left: 50%;
    transform: translate(-50%);
    margin-bottom: 10px;

    .el-dropdown-link {
      cursor: pointer;
      color: #fff;
    }
  }

  .el-menu {
    border-right: none;
    width: 100%;
  }
}

.el-main {
  background-color: #f9f9f9;
}
</style>
