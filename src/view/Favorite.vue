<template>
    <div class="Favorite-List">
        <h2>我的收藏</h2>
        <News
        v-for="items in favoritelist"
        :key="items.id"
        :news="items"
        />
        <el-empty
        v-if="f-list.length===0"
        description="暂无收藏"
        />
    </div>
</template>
<script setup>
import {ref,onMounted} from 'vue'
import News from'@/components/News'
import {getFavoriteList} from '@/api/news'
const favoritelist=ref([])
const loadFavorites=async()=>{
    const res=getFavoriteList()
    favoritelist=res.data
}
onMounted(()=>{
    loadFavorites()
})

</script>
<style scoped>
.Favorite-List {
  padding: 16px;
}
</style>