<template>
    <div class="history">
        <h2>浏览历史</h2>
        <News
        v-for="items in historylist"
        :key="items.id"
        :news="items"
        />
        <el-empty
        v-if="h-list.length===0"
        description="暂无浏览历史"
        />
    </div>
</template>
<script setup>
import{ref,onMounted} from 'vue'
import {Elmessage} from 'element-plus'
import {getHistoryList,removeHistory} from'@/api/news'
const historylist=ref([])
const loadHistory=async()=>{
    const res= await getHistoryList()
    historylist.value=res.data
}
const removeHistory=async(id)=>{
    await removeHistory(id)
    historylist.value=historylist.value.filter(item=>item.id!==id)
}//先通知后端删除历史，再从页面上删除，删除的逻辑是通过filter创建新数组，如果原数组中的id与所给的id不相等就留下，间接去掉历史记录
onMounted(()=>{
    loadHistory()
})

</script>
<style scoped>
.history {
  max-width: 800px;
}
</style>