<script lang="ts" setup>
import { onMounted } from "vue";
import { useUserStore } from "@/store/user.js";
import http from "@/utils/requests.js";
import Swal from "sweetalert2";
import CalHeatmap from "cal-heatmap";
import "cal-heatmap/cal-heatmap.css";
import Tooltip from "cal-heatmap/plugins/Tooltip";
import LegendLite from "cal-heatmap/plugins/LegendLite";

const cal: CalHeatmap = new CalHeatmap();

const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const currentMonth = currentDate.getMonth() + 1;

let heatmap: any[] = [];
const userStore = useUserStore();
const uid = userStore.user?.uid;

async function getHotMap() {
  try {
    const response = await http.request({
      method: "GET",
      url: `/api/hotmap?uid=${encodeURIComponent(uid)}`,
    });
    if (response.status === 200) {
      let result = Object.entries(response.data.docs);
      heatmap = [];
      for (let [key, value] of result) {
        heatmap.push({ date: key, num: value });
      }
      setHotMap();
    }
  } catch (error) {
    await Swal.fire({
      text: "获取热力图失败",
      icon: "error",
      position: "top",
      toast: true,
      timer: 2000,
      timerProgressBar: true,
    });
  }
}

// 设置每页展示的月份数量
const monthsPerPage = 4;

// 计算当前页的起始日期和结束日期
const startDate = new Date(currentYear, currentMonth - 3, 1); // 月份从 0 开始，因此要减 1
const minDate = new Date(currentYear - 1, currentMonth, 1);
const maxDate = new Date(currentYear, currentMonth, 1);

function setHotMap() {
  cal.paint(
    {
      data: {
        source: heatmap,
        type: "json",
        x: "date",
        y: "num",
      },
      date: { start: startDate, min: minDate, max: maxDate },
      range: monthsPerPage,
      scale: {
        color: {
          type: "threshold",
          range: ["#4dd05a", "#37a446", "#166b34", "#14432a"],
          domain: [1, 5, 10, 20],
        },
      },
      domain: {
        type: "month",
        gutter: 10,
        label: { text: "MMM", position: "bottom" },
      },
      subDomain: {
        type: "day",
        radius: 5,
        width: 18,
        height: 18,
        gutter: 3,
      },
      itemSelector: "#cal-heatmap",
    },
    [
      [
        Tooltip,
        {
          text: function (date: any, value: any, dayjsDate: any) {
            return (
              (value ? value : "没有") +
              " 文档在" +
              dayjsDate.format("YYYY, MMMM D, dddd")
            );
          },
          itemSelector: "#cal-heatmap",
        },
      ],
      [
        LegendLite,
        {
          includeBlank: true,
          itemSelector: "#ex-ghDay-legend",
          radius: 2,
          width: 11,
          height: 11,
          gutter: 4,
        },
      ],
    ],
  );
}

function preMonth() {
  cal.previous(3);
}

function nextMonth() {
  cal.next(3);
}

onMounted(() => {
  if (uid) {
    getHotMap();
  }
});
</script>

<template>
  <div class="m-2 flex justify-center">
    <div id="cal-heatmap"></div>
  </div>
  <div class="pl-4 pr-4">
    <a class="m-4 inline-block hover:text-[--dark-orange]" @click="preMonth">
      <i class="iconfont icon-shangyige text-2xl"></i
    ></a>
    <a class="m-4 inline-block hover:text-[--dark-orange]" @click="nextMonth">
      <i class="iconfont icon-xiayige text-2xl"></i
    ></a>
    <div style="float: right; font-size: 0.9rem; margin: 1rem">
      <span style="color: #768390; margin-right: 2px">Less</span>
      <div id="ex-ghDay-legend" style="display: inline-block"></div>
      <span style="color: #768390; margin-left: 2px">More</span>
    </div>
  </div>
</template>

<style>

</style>
