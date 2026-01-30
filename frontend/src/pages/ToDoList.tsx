import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import itemsApi from "../api/items";
import type { Item } from "../api/items";
import styles from "./ToDoList.module.css";

export default function ToDoList() {
  const { id: listId } = useParams<{ id: string }>();

  const [items, setItems] = useState<Item[]>([]);
  const [text, setText] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (!listId) return;

    const fetchItems = async () => {
      const data = await itemsApi.getItems(listId, page, 10);
      setItems(data.items);
    };

    fetchItems();
  }, [listId, page]);

  const addItem = async () => {
  if (!text.trim() || !listId) return;

  await itemsApi.createItem(listId, { text });
  setText("");
  setPage(1);

  const data = await itemsApi.getItems(listId, 1, 10);
  setItems(data.items);
};


  const toggleItem = async (item: Item) => {
    await itemsApi.updateItem(item.id, {
      completed: !item.completed,
    });

    const data = await itemsApi.getItems(listId!, page, 10);
    setItems(data.items);
  };

  const removeItem = async (id: string) => {
    await itemsApi.deleteItem(id);

    const data = await itemsApi.getItems(listId!, page, 10);
    setItems(data.items);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1>Todo Items</h1>
        <p>Manage tasks in this list</p>
      </header>

      <div className={styles.create}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="New task"
        />
        <button onClick={addItem}>Add</button>
      </div>

      <ul className={styles.list}>
        {items.map((item) => (
          <li
            key={item.id}
            className={`${styles.item} ${
              item.completed ? styles.completed : ""
            }`}
          >
            <input
              type="checkbox"
              checked={item.completed}
              onChange={() => toggleItem(item)}
            />
            <span>{item.text}</span>
            <button onClick={() => removeItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <div className={styles.pagination}>
        <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>
          Prev
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage((p) => p + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}
