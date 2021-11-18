import { shallowMount } from '@vue/test-utils'
import Employee from '@/views/Employee.vue'

test('triggers a click', async () => {
  const wrapper = shallowMount(Employee)

  await wrapper.find('nc-button').trigger('click')
})


