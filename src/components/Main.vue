<template>
<div>
  <ul class="nav justify-content-end">
    <li class="nav-item">
      <div :title="replication.info" class="text-muted">
        <span class="ti-server"></span>
        <span v-if="replication.state == 'paused' " class="ti-control-pause"></span>
        <span v-if="replication.state == 'active' " class="ti-pulse"></span>
        <span v-if="replication.state == 'denied' " class="ti-na"></span>
        <span v-if="replication.state == 'complete' " class="ti-check"></span>
        <span v-if="replication.state == 'error' " class="ti-bolt"></span>
      </div>
    </li>
  </ul>
  <div v-if='accepted' class='alert alert-success'>Eintrag angenommen.</div>
  <wizard v-if='ready' @submit='newEntry' />
  <div v-else class="jumbotron">
    <h1>Bitte einloggen</h1>

    <form @submit='submit'>
     <vue-form-generator :model="model" 
                         :schema="schema"
                         :options="formOptions"
                         >
                           
     </vue-form-generator>
     <button type="submit" class="btn btn-primary">Einloggen</button>
    </form>
  </div>
</div>
</template>

<script>
import VueFormGenerator from 'vue-form-generator'
// import VueFormWizard from 'vue-form-wizard'
import PouchDB from 'pouchdb'
import Wizard from './Wizard'
import uuid from 'uuid'

import 'vue-form-wizard/dist/vue-form-wizard.min.css'

const db = new PouchDB('collector')

function makeModel () {
  return {
    person: '',
    place: '',
    password: ''
  }
}

export default {
  name: 'main',
  components: {
    'wizard': Wizard
  },
  data () {
    return {
      model: makeModel(),
      ready: false,
      accepted: false,
      db: db,
      remote: null,
      replication: {
        state: null,
        info: null
      },
      schema: {
        fields: [{
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          label: 'Name',
          model: 'person',
          hint: 'Login Name',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6'
        },
        {
          type: 'input',
          inputType: 'password',
          autocomplete: false,
          label: 'Passwort',
          model: 'password',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6'
        },
        {
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          label: 'Ort',
          model: 'place',
          hint: 'Wo wird gerade gesammelt? Ort, Stadt, aber mindestens Bundesland',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6'
        }
        ]
      },
      formOptions: {
        validationErrorClass: 'has-error',
        validationSuccessClass: 'has-success',
        validateAfterChanged: true
      }
    }
  },
  methods: {
    submit () {
      const remote = new PouchDB('https://cllctrdb.bewegung.jetzt/cllctr/', {
        ajax: {
          cache: false,
          withCredentials: true
        },
        skip_setup: true,
        auth: {
          username: 'cllctr',
          password: this.$data.model.password
        }
      })

      this.$data.db.replicate.to(remote, {
        live: true,
        retry: true
      }).on('paused', (err) => {
      // replication paused (e.g. replication up to date, user went offline)
        this.$data.replication.state = 'paused'
        this.$data.replication.info = err
      }).on('active', () => {
      // replicate resumed (e.g. new changes replicating, user went back online)
        this.$data.replication.state = 'active'
        this.$data.replication.info = null
      }).on('denied', (err) => {
      // a document failed to replicate (e.g. due to permissions)
        this.$data.replication.state = 'denied'
        this.$data.replication.info = err
      }).on('complete', (info) => {
        this.$data.replication.state = 'complete'
        this.$data.replication.info = info
      // handle complete
      }).on('error', (err) => {
        this.$data.replication.state = 'error'
        this.$data.replication.info = err
      // handle error
      })

      this.$data.ready = true
      console.log('test')
    },
    newEntry (model) {
      model._id = uuid()
      model.added = {
        by: this.$data.model.person,
        at: this.$data.model.place,
        when: (new Date()).toISOString()
      }

      this.$data.ready = false
      db.put(model).then(() => {
        this.$data.accepted = true
        this.$data.ready = true
      })
    }
  }
}
</script>