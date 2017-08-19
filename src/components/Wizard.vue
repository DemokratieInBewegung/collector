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
           <h2>Hallo</h2>
           <p>Hättest Du eventuell Interesse an weiteren Informationen zu DiB und unseren Spitzenkandidat/innen?</p>
           <p>Natürlich werden diese vertraulich und nach strengsten Deutschen Datenrichtlinien behandelt. Die Daten werden nicht an Dritte veräußert und ausschließlich von DiB für die vereinbarte Kommunikation benutzt.</p>
           <vue-form-generator :model="model" 
                               :schema="firstTabSchema"
                               :options="formOptions"
                               ref="firstTabForm"
                               >
                                 
           </vue-form-generator>
        </tab-content>
        <tab-content title="Kontakt"
                     icon="ti-id-badge" :before-change="validateSecondTab">
          <p>Ist es okay, wenn ich nach deiner E-Mail Addresse frage? Unsere Spitzenkandidatin (NAME) würde sich gerne bei dir für die Unterstützung bedanken!</p>
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
import 'vue-form-wizard/dist/vue-form-wizard.min.css'

function makeModel () {
  return {
    type: 'contact',
    firstname: '',
    lastname: '',
    email: '',
    newsletter: true,
    zipcode: '',
    mobile: '',
    whatsapp: false,
    gender: '',
    agegroup: '< 25',
    confidence: 0,
    score: 0,
    'pot-volunteer': false,
    'pot-bewegerin': false,
    'pot-member': false
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
          model: 'firstname',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6 offset-md-3'
        },
        {
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          placeholder: 'Nachname',
          model: 'lastname',
          required: true,
          validator: VueFormGenerator.validators.string,
          styleClasses: 'col-md-6 offset-md-3'
        },
        {
          type: 'input',
          inputType: 'text',
          autocomplete: false,
          placeholder: 'Postleitzahl',
          model: 'zipcode',
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
            label: ' Newsletter',
            hint: ' Möchtest Du weitere Informationen von DiB und unseren Inhalten bekommen? Dann würden wir die Adresse auch auf dem Newsletter eintragen. Andernfalls natürlich nicht.',
            model: 'newsletter',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          },
          {
            type: 'input',
            inputType: 'text',
            autocomplete: false,
            placeholder: ' Handy Nummer',
            model: 'mobile',
            hint: ' Und/Oder Hast Du eine WhatsApp-Nummer unter der Dich die Spitzenkandidatin (NAME) unter Umständen erreichen kann?',
            required: false,
            validator: VueFormGenerator.validators.string,
            styleClasses: 'col-md-6 offset-md-3'
          },
          {
            type: 'checkbox',
            label: ' Whatsapp',
            model: 'whatsapp',
            hint: 'abwählen, falls kein whatsapp',
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
            label: 'Promoter Score',
            hint: 'Wie wahrscheinlich ist es, dass Du DEMOKRATIE In BEWEGUNG an einen anderen Freund oder Bekannten weiter empfehlen wirst? Skala 1-10, wobei 0=keinesfalls und 10=umgehend und auf jeden Fall ',
            model: 'score',
            required: false,
            styleClasses: 'col-md-6 offset-md-3 h4',
            values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
          },
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
            model: 'agegroup',
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
            type: 'checkbox',
            label: ' Freiwillige/r',
            hint: 'hat interesse signalisiert, als Freiwillige/r für uns aktiv zu werden',
            model: 'pot-volunteer',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          },
          {
            type: 'checkbox',
            label: ' Beweger/in',
            model: 'pot-bewegerin',
            hint: 'hat interesse signalisiert Beweger/in werden',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          },
          {
            type: 'checkbox',
            label: ' Mitglied',
            model: 'pot-member',
            hint: 'hat interesse signalisiert Mitglied werden',
            default: true,
            styleClasses: 'col-md-6 offset-md-3 form-inline'
          },
          {
            type: 'radios',
            autocomplete: false,
            label: 'Wird-uns-wählen-Einschätzung:',
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
      this.$emit('submit', model)
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
