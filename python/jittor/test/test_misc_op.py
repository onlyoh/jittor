
# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers: 
#     Wenyang Zhou <576825820@qq.com>
#     Dun Liang <randonlang@gmail.com>. 
# 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import unittest
import jittor as jt
import numpy as np
import jittor.nn as jnn

skip_this_test = False

try:
    jt.dirty_fix_pytorch_runtime_error()
    import torch
    import torch.nn as tnn
    import torchvision
except:
    torch = None
    tnn = None
    torchvision = None
    skip_this_test = True

def check_equal(res1, res2, eps=1e-5):
    assert np.allclose(res1.detach().numpy(), res2.numpy(), eps)

@unittest.skipIf(skip_this_test, "No Torch found")
class TestPad(unittest.TestCase):
    def test_index_add_(self):
        x = np.ones((5,3))
        a1 = torch.Tensor(x)
        a1.index_add_(0, torch.tensor([0,4,2]), torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=torch.float))
        a2 = jt.array(x)
        a2.index_add_(0, jt.array([0,4,2]), jt.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        check_equal(a1, a2)

        x = np.ones((3,5))
        a1 = torch.Tensor(x)
        a1.index_add_(1, torch.tensor([0,4,2]), torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=torch.float))
        a2 = jt.array(x)
        a2.index_add_(1, jt.array([0,4,2]), jt.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        check_equal(a1, a2)
        print('pass index_add_ test ...')

    def test_repeat(self):
        arr = np.random.randn(16,3,224,224)
        check_equal(torch.Tensor(arr).repeat(1,2,3,4), jt.array(arr).repeat(1,2,3,4))
        check_equal(torch.Tensor(arr).repeat(4,2,3,4), jt.array(arr).repeat(4,2,3,4))
        print('pass repeat test ...')

    def test_chunk(self):
        arr = np.random.randn(16,3,224,224)
        check_equal(torch.Tensor(arr).chunk(2,0)[0], jt.array(arr).chunk(2,0)[0])
        check_equal(torch.Tensor(arr).chunk(2,0)[1], jt.array(arr).chunk(2,0)[1])
        print('pass chunk test ...')
    
    def test_stack(self):
        arr1 = np.random.randn(16,3,224,224)
        arr2 = np.random.randn(16,3,224,224)
        check_equal(torch.stack([torch.Tensor(arr1), torch.Tensor(arr2)], 0), jt.stack([jt.array(arr1), jt.array(arr2)], 0))
        print('pass stack test ...')

    def test_flip(self):
        arr = np.random.randn(16,3,224,224)
        check_equal(torch.Tensor(arr).flip(0), jt.array(arr).flip(0))
        check_equal(torch.Tensor(arr).flip(1), jt.array(arr).flip(1))
        check_equal(torch.Tensor(arr).flip(2), jt.array(arr).flip(2))
        check_equal(torch.Tensor(arr).flip(3), jt.array(arr).flip(3))
        check_equal(torch.Tensor(arr).flip([2,3]), jt.array(arr).flip([2,3]))
        print('pass flip test ...')

    def test_cross(self):
        arr1 = np.random.randn(16,3,224,224,3)
        arr2 = np.random.randn(16,3,224,224,3)
        check_equal(torch.Tensor(arr1).cross(torch.Tensor(arr2), dim=1), jt.array(arr1).cross(jt.array(arr2), dim=1), 1e-1)
        check_equal(torch.Tensor(arr1).cross(torch.Tensor(arr2), dim=-4), jt.array(arr1).cross(jt.array(arr2), dim=-4), 1e-1)
        check_equal(torch.Tensor(arr1).cross(torch.Tensor(arr2), dim=-1), jt.array(arr1).cross(jt.array(arr2), dim=-1), 1e-1)
        check_equal(torch.Tensor(arr1).cross(torch.Tensor(arr2), dim=4), jt.array(arr1).cross(jt.array(arr2), dim=4), 1e-1)
        print('pass cross test ...')

    def test_normalize(self):
        arr = np.random.randn(16,3,224,224,3)
        check_equal(tnn.functional.normalize(torch.Tensor(arr)), jt.normalize(jt.array(arr)))
        check_equal(tnn.functional.normalize(torch.Tensor(arr), dim=0), jt.normalize(jt.array(arr), dim=0), 1e-1)
        check_equal(tnn.functional.normalize(torch.Tensor(arr), dim=1), jt.normalize(jt.array(arr), dim=1), 1e-1)
        check_equal(tnn.functional.normalize(torch.Tensor(arr), dim=-1), jt.normalize(jt.array(arr), dim=-1), 1e-1)
        check_equal(tnn.functional.normalize(torch.Tensor(arr), dim=2), jt.normalize(jt.array(arr), dim=2), 1e-1)
        check_equal(tnn.functional.normalize(torch.Tensor(arr), dim=3), jt.normalize(jt.array(arr), dim=3), 1e-1)
        print('pass normalize test ...')

    def test_make_grid(self):
        arr = np.random.randn(16,3,10,10)
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr)), jt.make_grid(jt.array(arr)))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=2), jt.make_grid(jt.array(arr), nrow=2))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=3), jt.make_grid(jt.array(arr), nrow=3))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=3, padding=4), jt.make_grid(jt.array(arr), nrow=3, padding=4))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=3, padding=4, pad_value=-1), jt.make_grid(jt.array(arr), nrow=3, padding=4, pad_value=-1))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=3, normalize=True, padding=4, pad_value=-1), jt.make_grid(jt.array(arr), nrow=3, normalize=True, padding=4, pad_value=-1))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), nrow=3, normalize=True, padding=4, pad_value=-1, range=(-100,100)), jt.make_grid(jt.array(arr), nrow=3, normalize=True, padding=4, pad_value=-1, range=(-100,100)))
        print('pass make_grid test ...')

    def test_make_grid2(self):
        def check(shape):
            arr = np.random.randn(*shape)
            check_equal(torchvision.utils.make_grid(torch.Tensor(arr)), jt.make_grid(jt.array(arr)))
        check((3,100,200))
        check((1,100,200))
        check((100,200))
        check((1,3,100,200))
        check((4,3,100,200))
        check((10,3,100,200))

    def test_make_grid3(self):
        arr=np.random.randn(3,10,10)
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr)), jt.make_grid(jt.array(arr)))
        check_equal(torchvision.utils.make_grid(torch.Tensor(arr), normalize=True), jt.make_grid(jt.array(arr), normalize=True))

    def test_save_image(self):
        arr = jt.array(np.random.randn(16,3,10,10))
        jt.save_image(arr, jt.flags.cache_path+"/tmp/a.jpg")

    def test_unbind(self):
        arr = np.random.randn(2,3,4)
        for dim in range(len(arr.shape)):
            t_res = torch.unbind(torch.Tensor(arr), dim=dim)
            j_res = jt.unbind(jt.array(arr), dim=dim)
            for idx in range(len(t_res)):
                assert np.allclose(t_res[idx].numpy(), j_res[idx].numpy())
        print('pass unbind test ...')

    def test_expand(self):
        a = jt.zeros((3,1))
        b = a.expand(3, 4)
        assert b.shape == (3,4)
        b = a.expand(-1, 4)
        assert b.shape == (3,4)
        b = a.expand((3, 4))
        assert b.shape == (3,4)
        b = a.expand((-1, 4))
        assert b.shape == (3,4)

    def test_bilinear(self):
        from jittor import nn
        m = nn.Bilinear(20, 30, 40)
        input1 = jt.randn(128, 20)
        input2 = jt.randn(128, 30)
        output = m(input1, input2)
        assert output.shape == [128,40]

        m2 = torch.nn.Bilinear(20, 30, 40)
        m2.weight = torch.nn.Parameter(torch.Tensor(m.weight.data))
        m2.bias = torch.nn.Parameter(torch.Tensor(m.bias.data))
        in1 = torch.Tensor(input1.data)
        in2 = torch.Tensor(input2.data)
        out = m2(in1, in2)
        np.testing.assert_allclose(
            out.detach().numpy(), output.data,
            atol=1e-4)

    def test_ctc_loss(self):
        def check(T,C,N,S,S_min):
            jt.set_global_seed(0)

            # Initialize random batch of input vectors, for *size = (T,N,C)
            input = jt.randn(T, N, C).log_softmax(2)
            # input = -jt.ones((T, N, C))
            # input[0,0,1] += 0.01

            # Initialize random batch of targets (0 = blank, 1:C = classes)
            target = jt.randint(low=1, high=C, shape=(N, S), dtype=jt.int)
            _input_jt = input

            input_lengths = jt.full((N,), T, dtype=jt.int)
            target_lengths = jt.randint(low=S_min, high=S+1, shape=(N,), dtype=jt.int)
            # ctc_loss = nn.CTCLoss()
            loss = jt.ctc_loss(input, target, input_lengths, target_lengths, reduction='none')
            _loss_jt = loss

            loss_jt = loss.numpy()

            input = torch.Tensor(input.numpy()).detach().requires_grad_()
            input_lengths = torch.full(size=(N,), fill_value=T, dtype=torch.long)
            target_lengths = torch.LongTensor(target_lengths.numpy())
            input_lengths = torch.LongTensor(input_lengths.numpy())
            target = torch.LongTensor(target.numpy())
            loss = tnn.CTCLoss(reduction='none')(input, target, input_lengths, target_lengths)
            np.testing.assert_allclose(loss.detach().numpy(), loss_jt, rtol=1e-5, atol=1e-5)

            dinput_jt = jt.grad(_loss_jt, _input_jt)
            dinput_jt.sync()

            loss.sum().backward()
            # print(input.grad)
            # print(dinput_jt)
            # print(loss)

        def check_gpu_with_cpu(T,C,N,S,S_min):
            jt.set_global_seed(1)

            # Initialize random batch of input vectors, for *size = (T,N,C)
            input = jt.randn(T, N, C).log_softmax(2)
            # input = -jt.ones((T, N, C))
            # input[0,0,1] += 0.01

            # Initialize random batch of targets (0 = blank, 1:C = classes)
            target = jt.randint(low=1, high=C, shape=(N, S), dtype=jt.int)
            _input_jt = input

            input_lengths = jt.full((N,), T, dtype=jt.int)
            target_lengths = jt.randint(low=S_min, high=S+1, shape=(N,), dtype=jt.int)
            # ctc_loss = nn.CTCLoss()
            loss = jt.ctc_loss(input, target, input_lengths, target_lengths, reduction='none')
            _loss_jt = loss

            loss_jt = loss.numpy()

            dinput_jt = jt.grad(_loss_jt, _input_jt)
            dinput_jt.sync()

            with jt.flag_scope(use_cuda=1):
                input = input.copy()
                target = target.copy()
                input_lengths = input_lengths.copy()
                target_lengths = target_lengths.copy()
                loss = jt.ctc_loss(input, target, input_lengths, target_lengths, reduction='none')
                grad = jt.grad(loss, input)
                np.testing.assert_allclose(_loss_jt.numpy(), loss.numpy(), atol=1e-5, rtol=1e-5)
                np.testing.assert_allclose(dinput_jt.numpy(), grad.numpy(), atol=1e-5, rtol=1e-5)


        check(2,2,1,1,1)
        check(50,20,16,30,10)

        if jt.has_cuda:
            with jt.flag_scope(use_cuda=1):
                check(2,2,1,1,1)
                check(50,20,16,30,10)
            check_gpu_with_cpu(50,20,16,30,10)

class TestOther(unittest.TestCase):
    def test_save(self):
        pp = [1,2,jt.array([1,2,3]), {"a":[1,2,3], "b":jt.array([1,2,3])}]
        name = jt.flags.cache_path+"/xx.pkl"
        jt.save(pp, name)
        x = jt.load(name)
        assert x[:2] == [1,2]
        assert (x[2] == np.array([1,2,3])).all()
        assert x[3]['a'] == [1,2,3]
        assert (x[3]['b'] == np.array([1,2,3])).all()

    def test_arctan2(self):
        a = jt.arctan2(jt.array([1,1.0,0]), jt.array([1,0.0,-1]))
        np.testing.assert_allclose(a.data, [0.7853982,1.5707964,3.1415927])

if __name__ == "__main__":
    unittest.main()