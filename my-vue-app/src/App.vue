<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <header class="bg-green-500 text-white p-4">
      <h1 class="text-xl">房产管理系统</h1>
    </header>

    <main class="p-6">
      <!-- 显示路由对应的页面组件 -->
      <router-view />
    </main>

    <footer class="bg-gray-200 text-center text-sm py-4 mt-10">
      © 2025 房产管理系统
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
body {
  margin: 0;
  font-family: "Helvetica Neue", sans-serif;
}
</style>