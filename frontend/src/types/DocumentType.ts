export type Document = {
  _id?: string;
  title: string;
  share_id: string;
  is_shared: boolean;
  createTime: string;
  updateTime: string;
  tag: string;
  tag_color?: string;
  content?: string;
};

export type renameType = {
  _id: string;
  newTitle: string;
}