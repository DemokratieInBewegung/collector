<template>
  <div>
    <form-wizard @on-complete="onComplete"
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
        <tab-content title="Kontakt Info"
                     icon="ti-id-badge" :before-change="submitModel">
         <vue-form-generator :model="model" 
                               :schema="secondTabSchema"
                               :options="formOptions"
                               ref="secondTabForm"
                               >                                
           </vue-form-generator>
           
        </tab-content>
        <tab-content title="Danke"
                     icon="ti-heart">
          <h4>Your json is ready!</h4>
          <div class="panel-body">
            <pre v-if="model" v-html="prettyJSON(model)"></pre>
          </div>
        </tab-content>
    </form-wizard>
  </div>
</template>

<script>
import VueFormGenerator from 'vue-form-generator'
// import VueFormWizard from 'vue-form-wizard'

import 'vue-form-wizard/dist/vue-form-wizard.min.css'

export default {
  name: 'wizard',
  data () {
    return {
      model: {
        firstName: '',
        lastName: '',
        email: '',
        newsletter: true,
        postal_code: '',
        phone_number: ''
      },
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
          }
        ]
      }
    }
  },
  methods: {
    onComplete: function () {
      alert('Yay. Done!')
    },
    validateFirstTab: function () {
      return this.$refs.firstTabForm.validate()
    },
    validateSecondTab: function () {
      return this.$refs.secondTabForm.validate()
    },
    submitModel: function () {
      console.log(this)
      let validated = this.validateSecondTab()
      if (!validated) return validated
      console.log(this.model)
    },
    prettyJSON: function (json) {
      if (json) {
        json = JSON.stringify(json, undefined, 4)
        json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\\-]?\d+)?)/g, function (match) {
          var cls = 'number'
          if (/^"/.test(match)) {
            if (/:$/.test(match)) {
              cls = 'key'
            } else {
              cls = 'string'
            }
          } else if (/true|false/.test(match)) {
            cls = 'boolean'
          } else if (/null/.test(match)) {
            cls = 'null'
          }
          return '<span class="' + cls + '">' + match + '</span>'
        })
      }
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
