import Swal from "sweetalert2";

export function useUnSelect() {
  function unSelect() {
    Swal.fire({
      text: "当前未选中文档，请先选择！",
      toast: true,
      position: "top",
      icon: "error",
      showConfirmButton: true,
      timer: 3000,
      timerProgressBar: true,
      allowOutsideClick: true,
    });
  }
  return { unSelect };
}
