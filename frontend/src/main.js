import { createApp } from 'vue'

import App from './App.vue'

import router from './router'

import './style.css'

import ECharts from 'vue-echarts'
import "echarts-wordcloud"
import { use } from 'echarts/core'

import { CanvasRenderer } from 'echarts/renderers'

import {
    PieChart,
    BarChart
} from 'echarts/charts'

import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    DatasetComponent
} from 'echarts/components'

use([
    CanvasRenderer,

    PieChart,
    BarChart,

    TitleComponent,
    TooltipComponent,
    LegendComponent,

    GridComponent,
    DatasetComponent
])

const app = createApp(App)

app.component('v-chart', ECharts)

app.use(router)

app.mount('#app')