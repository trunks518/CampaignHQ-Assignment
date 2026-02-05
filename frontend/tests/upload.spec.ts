import { mount } from '@vue/test-utils'
import Upload from '../src/components/Upload.vue'

describe('Upload.vue', () => {
  it('renders summary after successful upload', async () => {
    const summary = {
      total_rows: 7,
      valid_rows: 3,
      by_status: { success: 1, fail: 1, unknown: 1 },
      errors: [{ row: 5, reason: 'invalid status' }],
    }

    // @ts-expect-error test env mock
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve(summary) })

    const wrapper = mount(Upload)
    const csv = 'id,status,ts,notes\n1,success,2024-01-01T00:00:00Z,a\n'
    const file = new File([csv], 'data.csv', { type: 'text/csv' })

    // call exposed method directly
    // @ts-expect-error exposed for test
    await wrapper.vm.uploadFile(file)

    expect(wrapper.text()).toContain('Total rows: 7')
    expect(wrapper.text()).toContain('Valid rows: 3')
    expect(wrapper.text()).toContain('success: 1')
    expect(wrapper.text()).toContain('fail: 1')
    expect(wrapper.text()).toContain('unknown: 1')
  })
})

