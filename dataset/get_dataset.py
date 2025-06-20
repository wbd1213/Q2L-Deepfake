import torchvision.transforms as transforms
from .cocodataset import CoCoDataset
from ..utils.cutout import SLCutoutPIL
from randaugment import RandAugment
import os.path as osp

def get_datasets(args):
    if args.orid_norm:
        normalize = transforms.Normalize(mean=[0, 0, 0], std=[1, 1, 1])
    else:
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    train_data_transform_list = [transforms.Resize((args.img_size, args.img_size)),
                                 RandAugment(),
                                 transforms.ToTensor(),
                                 normalize]
    try:
        # for q2l_infer scripts
        if args.cutout:
            print("Using Cutout!!!")
            train_data_transform_list.insert(1, SLCutoutPIL(n_holes=args.n_holes, length=args.length))
    except Exception as e:
        Warning(e)
    train_data_transform = transforms.Compose(train_data_transform_list)

    test_data_transform = transforms.Compose([transforms.Resize((args.img_size, args.img_size)),
                                              transforms.ToTensor(),
                                              normalize])
    

    if args.dataname == 'coco' or args.dataname == 'coco14':
        # ! config your data path here.
        dataset_dir = args.dataset_dir
        train_dataset = CoCoDataset(
            image_dir=osp.join(dataset_dir, 'train2014'),
            anno_path=osp.join(dataset_dir, 'annotations/instances_train2014.json'),
            input_transform=train_data_transform,
            labels_path='annotations/train_label_coco.npy',
        )
        val_dataset = CoCoDataset(
            image_dir=osp.join(dataset_dir, 'val2014'),
            anno_path=osp.join(dataset_dir, 'annotations/instances_val2014.json'),
            input_transform=test_data_transform,
            labels_path='annotations/val_label_coco.npy',
        )
        test_dataset = CoCoDataset(
            image_dir=osp.join(dataset_dir, 'test2014'),
            anno_path=osp.join(dataset_dir, 'annotations/instances_test2014.json'),
            input_transform=test_data_transform,
            labels_path='annotations/test_label_coco.npy',
        )

    else:
        raise NotImplementedError("Unknown dataname %s" % args.dataname)

    print("len(train_dataset):", len(train_dataset)) 
    print("len(val_dataset):", len(val_dataset))
    print("len(test_dataset):", len(test_dataset))
    return train_dataset, val_dataset, test_dataset
