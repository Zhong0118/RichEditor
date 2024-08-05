import Swal from "sweetalert2";
import { useDocumentStore } from "@/store/document";
import http from "@/utils/requests";
import emitter from "@/hooks/mitter.js";


const documentStore = useDocumentStore();

export function useShare() {
  async function shareState(flag) {
    try {
      const response = await http.request({
        method: "POST",
        url: "/api/share",
        data: {
          did: documentStore.document._id,
          flag: flag,
        },
      });
    } catch (error) {
      await Swal.fire({
        text: "共享失败",
        icon: "error",
        position: "top",
        toast: true,
        timer: 2000,
        timerProgressBar: true,
      });
    }
  }

  function shareDocument() {
    if (documentStore.document.is_shared) {
      Swal.fire({
        title: "本文档共享码",
        text: documentStore.document.share_id,
        confirmButtonText: "刷新",
        cancelButtonText: "关闭",
        denyButtonText: "取消共享",
        showConfirmButton: true,
        showCancelButton: true,
        showDenyButton: true,
      }).then((result) => {
        if (result.isConfirmed) {
          emitter.emit("refresh");
        } else if (result.isDenied) {
          shareCancel();
        }
      });
    } else {
      Swal.fire({
        text: "您确定共享文档吗",
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        showConfirmButton: true,
      }).then((result) => {
        if (result.isConfirmed) {
          documentStore.changeShared(true);
          shareState(true).then((r) =>
            Swal.fire({
              title: "本文档共享码",
              text: documentStore.document.share_id,
            }),
          );
        }
      });
    }
  }

  function shareCancel() {
    if (
      documentStore.document !== undefined &&
      documentStore.document.is_shared
    ) {
      documentStore.changeShared(false);
      shareState(false).then((r) =>
        Swal.fire({
          toast: true,
          timer: 2000,
          timerProgressBar: true,
          position: "top",
          icon: "info",
          text: documentStore.document.title + "取消共享",
        }),
      );
    }
  }

  return { shareDocument, shareCancel };
}
