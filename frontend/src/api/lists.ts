// src/api/lists.ts
import axiosClient from "../axiosClient";

export interface List {
  id: string;
  name: string;
}

export interface PaginatedLists {
  items: List[];
  page: number;
  total: number;
  page_size: number;
}

const listsApi = {
  getLists: async (
    page = 1,
    pageSize = 10
  ): Promise<PaginatedLists> => {
    const response = await axiosClient.get<PaginatedLists>(
      "/lists/",
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  createList: async (payload: { name: string }): Promise<List> => {
    const response = await axiosClient.post<List>(
      "/lists/",
      payload
    );
    return response.data;
  },

  deleteList: async (listId: string): Promise<void> => {
    await axiosClient.delete(`/lists/${listId}/`);
  },
};

export default listsApi;
