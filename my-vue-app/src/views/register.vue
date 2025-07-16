<template>
  <div>
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      用户名：<input v-model="form.username" required /><br />
      密码：<input v-model="form.password" type="password" required /><br />
      <input type="submit" value="注册" />
    </form>
    <router-link to="/login">已有账号？登录</router-link>
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
    async handleRegister() {
      const res = await fetch('http://localhost:5050/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      });

      if (res.ok) {
        alert('注册成功，请登录');
        this.$router.push('/login');
      } else {
        const data = await res.json();
        alert(data.message || '注册失败');
      }
    }
  }
};
</script>