// 导入所需的 PostCSS 插件
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

// 导出 PostCSS 配置对象
export default {
  plugins: [
    // 由于 tailwindcss 是一个函数，我们可以直接调用它并传入配置文件路径
    tailwindcss('./tailwind.config.js'),
    // autoprefixer 可以直接作为插件使用
    autoprefixer,
  ],
};