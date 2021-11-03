import { shallowMount } from '@vue/test-utils'
import Employee from '@/views/Employee.vue'

describe('Testing Component Employee', () => {
  test('is vue instance', () => {
    const wrapper = shallowMount(Employee)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('Test show form button', async () => {
    const wrapper = shallowMount(Employee)
    wrapper.find('#OpenFormButton').trigger('click')
    expect(wrapper.vm.$data.showForm).toBe(1)
  })

  test('Test submit form button', async () => {
    const wrapper = shallowMount(Employee)
    await wrapper.find('#OpenFormButton').trigger('click')
    await wrapper.find('#FormSubmitButton').trigger('click')
  })

  test('Test call of requestTimeoff method', async () => {
    const wrapper = shallowMount(Employee)
    const requestTimeoff = jest.fn()
    wrapper.setMethods({
      requestTimeoff: requestTimeoff
    })
    await wrapper.find('#OpenFormButton').trigger('click')
    await wrapper.find('#FormSubmitButton').trigger('click')

    expect(requestTimeoff).toBeCalled()
  })

  test('Test call of toFullDate method', async () => {
    const wrapper = shallowMount(Employee)
    const toFullDate = jest.fn()
    wrapper.setMethods({
      toFullDate: toFullDate
    })
    await wrapper.find('#OpenFormButton').trigger('click')
    await wrapper.find('#FormSubmitButton').trigger('click')

    expect(toFullDate).toBeCalled()
  })
})