import Vue from 'vue'

import './styles/quasar.sass'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import '@quasar/extras/material-icons-round/material-icons-round.css'
import '@quasar/extras/material-icons-sharp/material-icons-sharp.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'
import '@quasar/extras/ionicons-v4/ionicons-v4.css'
import '@quasar/extras/mdi-v4/mdi-v4.css'
import {
    Quasar,
    ClosePopup,
    QLayout,
    QHeader,
    QDrawer,
    QPageContainer,
    QPage,
    QToolbar,
    QToolbarTitle,
    QBtn,
    QIcon,
    QList,
    QItem,
    QItemSection,
    QItemLabel,
    QSelect,
    QTable,
    QTime,
    QTh,
    QTr,
    QTd,
    QCard,
    Dialog,
    Notify
} from 'quasar'

Vue.use(Quasar, {
  components: {
    QLayout,
    QHeader,
    QDrawer,
    QPageContainer,
    QPage,
    QToolbar,
    QToolbarTitle,
    QBtn,
    QIcon,
    QList,
    QItem,
    QItemSection,
    QItemLabel,
    QSelect,
    QTable,
    QTime,
    QTh,
    QTr,
    QTd,
    QCard,
  },
  directives: {
      ClosePopup
  },
  plugins: {
    Notify,
    Dialog,
  },
  config: {
    notify: { /* Notify defaults */ }
  }
 })