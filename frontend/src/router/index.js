import { createRouter, createWebHistory } from "vue-router";

import BookList from "../components/BookList.vue";
import BorrowBook from "../components/BorrowBook.vue";
import ReturnBook from "../components/ReturnBook.vue";
import Transactions from "../components/Transaction.vue";

const routes = [
  {
    path: "/",
    name: "books",
    component: BookList,
  },
  {
    path: "/borrow",
    name: "borrow",
    component: BorrowBook,
  },
  {
    path: "/return",
    name: "return",
    component: ReturnBook,
  },
  {
    path: "/transactions",
    name: "transactions",
    component: Transactions,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
