<template>
  <div>
    <form-wizard @on-complete="submitModel"
                 ref="wizard"
                 color="gray"
                 title="Kontakt Informationen eintragen"
                 subtitle="für DEMOKRATIE IN BEWEGUNG"
                 nextButtonText="Weiter"
                 backButtonText="Zurück"
                 finalButtonText="Abschicken"
                 error-color="#a94442"
                 >
        <tab-content title="Name"
                     icon="ti-user" :before-change="validateFirstTab">
           <vue-form-generator :model="model" 
                               :schema="firstTabSchema"
                               :options="formOptions"
                               ref="firstTabForm"
                               >
                                 
           </vue-form-generator>
        </tab-content>
        <tab-content title="Kontakt"
                     icon="ti-id-badge" :before-change="validateSecondTab">
         <vue-form-generator :model="model" 
                               :schema="secondTabSchema"
                               :options="formOptions"
                               ref="secondTabForm"
                               >                                
           </vue-form-generator>
           
        </tab-content>
        <tab-content title="Extras"
                     icon="ti-heart" :before-change="validateThirdTab">
          <h2>Deine Einschätzung zu der Person</h2>
            
           <vue-form-generator :model="model" 
                                 :schema="thirdTabSchema"
                                 :options="formOptions"
                                 ref="thirdTabForm"
                                 >                                
             </vue-form-generator>
        </tab-content>
    </form-wizard> 
  </div>
</template>

<script>
import VueFormGenerator from 'vue-form-generator'
// import VueFormWizard from 'vue-form-wizard'
import PouchDB from 'pouchdb'
import uuid from 'uuid'

import 'vue-form-wizard/dist/vue-form-wizard.min.css'

const db = new PouchDB('collector')
const remote = new PouchDB('https://cllctrdb.bewegung.jetzt/cllctr/', {
  ajax: {
    cache: false,
    withCredentials: true
  },
  skip_setup: true,
  auth: {
    username: 'cllctr',
    password: prompt('DB Password?')
  }
})

window.remote = remote

db.replicate.to(remote, {
  live: true,
  retry: true
})

function makeModel () {
  return {
    firstName: '',
    lastName: '',
    email: '',
    newsletter: true,
    postal_code: '',
    phone_number: '',
    whatsapp: false,
    gender: '',
    age: '< 25',
    confidence: 0
  }
}

export default {
  name: 'wizard',
  data () {
    return {
      model: makeModel(),
      formOptions: {
        validationErrorClass: 'has-error',
        validationSuccessClass: 'has-success',
        validateAfterChanged: true
      },
      firstTabSchema: {
        fields: [{
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          placeholder: 'Vorname',
          model: 'firstName',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6 offset-md-3'
        },
        {
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          placeholder: 'Nachname',
          model: 'lastName',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6 offset-md-3'
        },
        {
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          placeholder: 'Postleitzahl',
          model: 'postal_code',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6 offset-md-3'
        }
        ]
      },
      secondTabSchema: {
        fields: [
          {
            type: 'input',
            inputType: 'text',
            autocomplete: false,
            placeholder: 'Email',
            model: 'email',
            required: false,
            validator: VueFormGenerator.validators.email,
            styleClasses: 'col-md-6 offset-md-3 '
          },
          {
            type: 'checkbox',
            label: 'Bitte haltet mich über DiB auf dem Laufenden',
            model: 'newsletter',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          },
          {
            type: 'input',
            inputType: 'text',
            autocomplete: false,
            placeholder: 'Handy Nummer',
            model: 'phone_number',
            required: false,
            validator: VueFormGenerator.validators.string,
            styleClasses: 'col-md-6 offset-md-3'
          },
          {
            type: 'checkbox',
            label: 'Ist eine Whatsapp Nummer',
            model: 'whatsapp',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          }
        ]
      },
      thirdTabSchema: {
        fields: [
          {
            type: 'radios',
            autocomplete: false,
            label: 'Geschlecht',
            model: 'gender',
            required: false,
            styleClasses: 'col-md-6 offset-md-3 h4',
            values: [
               { name: 'Mann', value: 'm' },
               { name: 'Frau', value: 'f' },
               { name: 'Weder-noch', value: 'o' }]
          },
          {
            type: 'select',
            autocomplete: false,
            label: 'Alter (circa)',
            model: 'age',
            required: false,
            styleClasses: 'col-md-6 offset-md-3 h4',
            values: [
               { name: '< 25', value: '< 25' },
               { name: '25-35', value: '25-35' },
               { name: '35-45', value: '35-45' },
               { name: '45-55', value: '45-55' },
               { name: '55-65', value: '55-65' },
               { name: '65-75', value: '65-75' },
               { name: '> 75', value: '> 75' }]
          },
          {
            type: 'radios',
            autocomplete: false,
            label: 'Wird uns wählen Sicherheit:',
            model: 'confidence',
            required: false,
            styleClasses: 'col-md-6 offset-md-3 h3',
            values: [
               { name: ' ☹ ', value: 1 },
               { name: ' 😐 ', value: 2 },
               { name: ' 🤔 ', value: 3 },
               { name: ' 🙂 ', value: 4 },
               { name: ' 😍 ', value: 5 }]
          }
        ]
      }
    }
  },
  methods: {
    validateFirstTab: function () {
      return this.$refs.firstTabForm.validate()
    },
    validateSecondTab: function () {
      return this.$refs.secondTabForm.validate()
    },
    validateThirdTab: function () {
      return this.$refs.thirdTabForm.validate()
    },
    submitModel: function () {
      let model = JSON.parse(JSON.stringify(this.model))
      model._id = uuid()
      db.put(model).then(() => {
        this.$data.model = makeModel()
        this.$refs.wizard.navigateToTab(0)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
