<template>
  <div>
    <h2>新增房产</h2>
    <form @submit.prevent="handleSubmit">
      标题：<input v-model="form.title" required /><br />
      位置：<input v-model="form.location" required /><br />
      价格：<input v-model.number="form.price" required /><br />
      面积：<input v-model.number="form.size" required /><br />
      <input type="submit" value="提交" />
    </form>
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        title: '',
        location: '',
        price: 0,
        size: 0
      }
    };
  },
  methods: {
    async handleSubmit() {
      const res = await fetch('http://localhost:5050/api/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(this.form)
      });

      if (res.ok) {
        this.$router.push('/');
      } else {
        alert('提交失败，请重试');
      }
    }
  }
};
</script>