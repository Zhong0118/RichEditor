import http from "@/utils/requests";
import { useUserStore } from "@/store/user.ts";
import { useDocumentStore } from "@/store/document.ts";
import { ref } from "vue";
import Swal from "sweetalert2";

const userStore = useUserStore();
const documentStore = useDocumentStore();

function debounce(fn, wait, immediate) {
  let timeout;

  return function executedFunction(...args) {
    const context = this;

    if (timeout) clearTimeout(timeout);

    const later = () => {
      timeout = null;
      fn.apply(context, args);
    };

    const shouldCallNow = immediate && !timeout;

    timeout = setTimeout(later, wait);

    if (shouldCallNow) {
      // 如果 immediate 为 true，并且之前没有 timeout，则立即执行
      fn.apply(context, args);
    }
  };
}

export function useDocument() {
  const documentsList = ref([]);
  const create_did = ref("");
  const owner_id = userStore.user?.uid;

  async function createDocument(owner_id, doc) {
    try {
      const response = await http.request({
        method: "POST",
        url: "api/createdocument", // 假设你的API端点是/documents
        data: {
          owner_id: owner_id,
          doc: doc,
        },
      });
      if (response.status === 200) {
        await Swal.fire({
          text: "创建成功",
          icon: "success",
          toast: true,
          position: "top",
          timer: 2000,
          timerProgressBar: true,
        });
        const newDocument = {
          ...doc,
          _id: response.data.did,
        };
        documentsList.value.unshift(newDocument); // 将新文档添加到列表开头
        documentStore.setDocument(newDocument); // 更新 documentStore
      }
    } catch (error) {
      await Swal.fire({
        title: "创建失败",
        text: error.message,
        icon: "error",
        position: "top",
        toast: true,
        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  // 读取文档列表
  async function getAllDocuments() {
    try {
      const response = await http.request({
        method: "GET",
        url: `/api/getdocuments?owner_id=${encodeURIComponent(owner_id)}`,
      });
      if (response.status === 200) {
        documentsList.value = Object.values(response.data.documents); // 更新文档列表
      }
    } catch (error) {
      await Swal.fire({
        title: "获取文档列表失败",
        text: error.message,
        position: "top",
        icon: "error",
        toast: true,
        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  async function update_title(did, title, update) {
    try {
      const response = await http.request({
        method: "PUT",
        url: "api/rename",
        data: {
          did: did,
          title: title,
          update: update,
        },
      });
      if (response.status === 200) {
        await Swal.fire({
          text: "修改成功",
          icon: "success",
          toast: true,
          position: "top",

          timer: 2000,
          timerProgressBar: true,
        });
      }
    } catch (error) {
      await Swal.fire({
        text: "修改失败",
        icon: "error",
        toast: true,
        position: "top",

        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  async function update_tag(did, tag, update) {
    try {
      const response = await http.request({
        method: "PUT",
        url: "api/retag",
        data: {
          did: did,
          tag: tag,
          update: update,
        },
      });
      if (response.status === 200) {
        await Swal.fire({
          text: "修改成功",
          icon: "success",
          toast: true,
          position: "top",
          timer: 2000,
          timerProgressBar: true,
        });
      }
    } catch (error) {
      await Swal.fire({
        text: "修改失败",
        icon: "error",
        toast: true,
        position: "top",

        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  async function delete_doc(did) {
    try {
      const response = await http.request({
        method: "DELETE",
        url: "api/delete",
        data: {
          did: did,
        },
      });
      if (response.status === 200) {
        await Swal.fire({
          text: "删除成功",
          icon: "success",
          position: "top",
          toast: true,
          timer: 2000,
          timerProgressBar: true,
        });
      }
    } catch (error) {
      await Swal.fire({
        text: "删除失败",
        icon: "error",
        position: "top",
        toast: true,
        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  async function getContent() {
    if (documentStore.document) {
      try {
        // 使用 Axios 或其他 HTTP 客户端发送请求
        const response = await http.request({
          method: "GET",
          url: `/api/documents/content?did=${encodeURIComponent(documentStore.document._id)}`,
        });
        if (response.status === 200) {
          documentStore.document.content = response.data.text; // 更新文档内容
        }
      } catch (error) {
        // 处理错误
        await Swal.fire({
          text: "查找失败",
          icon: "error",
          position: "top",
          toast: true,
          timer: 2000,
          timerProgressBar: true,
        });
      }
    }
  }

  // 假设你有一个方法来处理 API 请求
  async function updateDocumentInDB() {
    if (documentStore.document) {
      try {
        // 使用 Axios 或其他 HTTP 客户端发送请求
        const response = await http.request({
          method: "POST",
          url: "/api/documents/update",
          data: {
            did: documentStore.document._id,
            update: new Date().toISOString(),
            content: documentStore.document.content,
          },
        });
        if (response.status === 200) {
          // 更新成功
          await Swal.fire({
            text: "保存成功",
            icon: "success",
            position: "top",
            toast: true,
            timer: 2000,
            timerProgressBar: true,
          });
        }
      } catch (error) {
        // 处理错误
        await Swal.fire({
          text: "保存失败",
          icon: "error",
          position: "top",
          toast: true,
          timer: 2000,
          timerProgressBar: true,
        });
      }
    }
  }

  const debounceUpdateDocumentInDB = debounce(updateDocumentInDB, 1000);
  const debounceGetContent = debounce(getContent, 1000);

  return {
    documentsList,
    create_did,
    getAllDocuments,
    createDocument,
    update_title,
    update_tag,
    delete_doc,
    debounceUpdateDocumentInDB,
    debounceGetContent,
    getContent,
  };
}
