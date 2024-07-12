import Swal from "sweetalert2";
import { useDocumentStore } from "@/store/document";

const documentStore = useDocumentStore();

export function useShare() {
  function shareDocument() {
    if (documentStore.document.is_shared) {
      Swal.fire({
        title: "本文档共享码",
        text: documentStore.document.share_id,
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
          Swal.fire({
            title: "本文档共享码",
            text: documentStore.document.share_id,
          });
        }
      });
    }
  }

  function shareCancel() {
    if (documentStore.document !== undefined && documentStore.document.is_shared ) {
      documentStore.changeShared(false);
      Swal.fire({
        toast: true,
        timer: 2000,
        timerProgressBar: true,
        position: "top",
        icon: "info",
        text: documentStore.document.title + "取消共享",
      });
    }
  }

  return { shareDocument, shareCancel };
}
