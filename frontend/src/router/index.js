import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import HomeView from '../views/HomeView.vue';
import BookListView from '../views/BookListView.vue';
import UserLoansView from '../views/UserLoansView.vue';
import ChangeDetailsView from '../views/ChangeDetailsView.vue';
import ManageBooksView from '../views/ManageBooksView.vue';
import ManageUsersView from '../views/ManageUsersView.vue';
import LoanHistoryView from '../views/LoanHistoryView.vue';
import { parseJwt } from '../utils/authUtils.js'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { path: '/', name: '/', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/books',
      name: 'books',
      component: BookListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/loans',
      name: 'loans',
      component: UserLoansView,
      meta: { requiresAuth: true },
    },
    {
      path: '/change-account-details',
      name: 'change-account-details',
      component: ChangeDetailsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/manage-books',
      name: 'manage-books',
      component: ManageBooksView,
      meta: { requiresAuth: true, requiresRole: 'librarian' },
    },
    {
      path: '/manage-users',
      name: 'manage-users',
      component: ManageUsersView,
      meta: { requiresAuth: true, requiresRole: 'librarian' },
    },
    {
      path: '/loans-history',
      name: 'loans-history',
      component: LoanHistoryView,
      meta: { requiresAuth: true, requiresRole: 'librarian' },
    },
  ],
});
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Online library';
  const token = localStorage.getItem('token');
  // Redirect to login if there's no token and the route requires authentication
  if (to.meta.requiresAuth && !token) {
    return next({ name: 'login' });
  }

  // Redirect to home if the user is logged in and tries to access login/register page
  if ((to.name === 'login' || to.name === 'register') && token) {
    return next({ name: 'home' });
  }

  // Check if the route requires a specific role and validate it
  if (to.meta.requiresRole && token) {
    const decodedToken = parseJwt(token);
    if (!decodedToken || decodedToken.role !== to.meta.requiresRole) {
      return next({ name: 'home' });
    }
  }

  // Proceed to the route
  next();
});

export default router;
