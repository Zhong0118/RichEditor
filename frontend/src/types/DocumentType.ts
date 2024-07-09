export type Document = {
  did: string;
  title: string;
  share_id?: string;
  is_shared?: boolean;
  createTime: string;
  updateTime: string;
  tag: string;
  tag_color: string;
  content?: string;
};

export type renameType = {
  did: string;
  newTitle: string;
}