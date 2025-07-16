<template>
  <div>
    <h2>欢迎，{{ username }}</h2>
    <a @click="logout" href="#">退出登录</a> |
    <router-link to="/create">新增房产</router-link>

    <h3>我的房产：</h3>
    <ul v-if="properties.length">
      <li v-for="p in properties" :key="p.id">
        {{ p.title }} - {{ p.location }} - {{ p.price }} 元 - {{ p.size }}㎡
        <button @click="deleteProperty(p.id)">删除</button>
      </li>
    </ul>
    <p v-else>您还没有添加房产。</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      properties: []
    };
  },
  async created() {
    const res = await fetch('http://localhost:5050/api/properties', {
      credentials: 'include'
    });
    if (res.ok) {
      const data = await res.json();
      this.username = data.username;
      this.properties = data.properties;
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    async deleteProperty(id) {
      if (!confirm('确定删除这条房产吗？')) return;
      const res = await fetch('http://localhost:5050/api/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ property_id: id })
      });
      if (res.ok) {
        this.properties = this.properties.filter(p => p.id !== id);
      } else {
        alert('删除失败');
      }
    },
    async logout() {
      await fetch('http://localhost:5050/api/logout', {
        credentials: 'include'
      });
      this.$router.push('/login');
    }
  }
};
</script>