//src/api/items.ts
import axiosClient from "../axiosClient";

export interface Item {
  id: string;
  text: string;
  completed: boolean;
  list_id: string;
}

export interface PaginatedItems {
  items: Item[];
  page: number;
  total: number;
  page_size: number;
}

const itemsApi = {
  getItems: async (
    listId: string,
    page = 1,
    pageSize = 10
  ): Promise<PaginatedItems> => {
    const response = await axiosClient.get<PaginatedItems>(
      `/items/list/${listId}`,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  createItem: async (
    listId: string,
    payload: { text: string }
  ): Promise<Item> => {
    const response = await axiosClient.post<Item>(
      `/items/list/${listId}`,
      payload
    );
    return response.data;
  },

  updateItem: async (
    itemId: string,
    payload: { text?: string; completed?: boolean }
  ): Promise<Item> => {
    const response = await axiosClient.patch<Item>(
      `/items/${itemId}`,
      payload
    );
    return response.data;
  },

  deleteItem: async (itemId: string): Promise<void> => {
    await axiosClient.delete(`/items/${itemId}`);
  },
};

export default itemsApi;
