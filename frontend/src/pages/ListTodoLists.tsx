import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import { Link } from "react-router-dom";
import listsApi from "../api/lists";
import type { List } from "../api/lists";
import styles from "./ListTodoLists.module.css";

export default function ListTodoLists() {
  const [lists, setLists] = useState<List[]>([]);
  const [name, setName] = useState("");
  const [page, setPage] = useState(1);

  const fetchLists = async (signal?: AbortSignal) => {
    try {
      const data = await listsApi.getLists(page, 10);
      if (!signal?.aborted) {
        setLists(data.items);
      }
    } catch (err) {
      if (signal?.aborted) return;
      console.error(err);
    }
  };

  useEffect(() => {
    const controller = new AbortController();
    fetchLists(controller.signal);
    return () => controller.abort();
  }, [page]);

  const addList = async () => {
    if (!name.trim()) return;
    await listsApi.createList({ name });
    setName("");
    fetchLists();
  };

  const deleteList = async (id: string) => {
    await listsApi.deleteList(id);
    fetchLists();
  };

  const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1>Your Lists</h1>
        <p>Manage your todo lists</p>
      </header>

      <div className={styles.create}>
        <input
          value={name}
          onChange={handleNameChange}
          placeholder="New list name"
        />
        <button type="button" onClick={addList}>
          Add
        </button>
      </div>

      <section className={styles.grid}>
        {lists.map((list) => (
          <div key={list.id} className={styles.card}>
            <Link to={`/lists/${list.id}`} className={styles.cardLink}>
              {list.name}
            </Link>

            <button
              type="button"
              className={styles.delete}
              onClick={() => deleteList(list.id)}
            >
              Delete
            </button>
          </div>
        ))}
      </section>

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
