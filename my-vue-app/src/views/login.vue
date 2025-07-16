<template>
  <div>
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      用户名：<input v-model="form.username" type="text" required /><br />
      密码：<input v-model="form.password" type="password" required /><br />
      <input type="submit" value="登录" />
    </form>
    <router-link to="/register">没有账号？注册</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: { username: '', password: '' }
    };
  },
  methods: {
    async handleLogin() {
      const res = await fetch('http://localhost:5050/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(this.form)
      });

      if (res.ok) {
        this.$router.push('/');
      } else {
        alert('用户名或密码错误，请重试。');
      }
    }
  }
};
</script>