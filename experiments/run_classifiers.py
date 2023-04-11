import numpy as np
import TCGA
from SignalTransformData.data_modules.simulated import SinusoidalDataModule
from configs.demo_config import get_demo_config

from WaveLSTM.models.classification import create_classifier


# TODO: make a proper configuration (.yaml or whatever)


def run_sinusoidal_example():

    # Load data and filter for only the cases of interest
    dm = SinusoidalDataModule(get_demo_config(), samples=2000, batch_size=256, sig_length=512,
                              save_to_file="/home/ubuntu/Documents/Notebooks/wave-LSTM_benchmark/sinusoidal.csv")
    print(dm)

    # Create model
    model, trainer = create_classifier(classes=[f"Class {i}" for i in range(6)],
                                       seq_length=512, strands=2, chromosomes=1,
                                       hidden_size=256, layers=1, proj_size=0, scale_embed_dim=128,
                                       recursion_limit=7,
                                       validation_hook_batch=next(iter(dm.val_dataloader())),  # TODO: update to all set
                                       test_hook_batch=next(iter(dm.test_dataloader())),       # TODO: update to all set
                                       run_id=f"demo",
                                       verbose=True
                                       )

    if True:
        trainer.fit(model, datamodule=dm)
        print(f"best checkpoint: {trainer.checkpoint_callback.best_model_path}")
    else:
        model = model.load_from_checkpoint(trainer.checkpoint_callback.dirpath + "/demo.ckpt")

    # Test model
    trainer.test(model, dataloaders=dm.test_dataloader())


def run_ascat_example():

    cancer_types = ['BRCA', 'OV']  # ['OV', 'GBM', 'KIRC', 'HNSC', 'LGG'],  # ,  #['STAD', 'COAD'],

    # Load data and filter for only the cases of interest
    dm = TCGA.data_modules.ascat.ASCATDataModule(batch_size=256, cancer_types=cancer_types)
    print(dm)

    # Create model
    model, trainer = create_classifier(classes=cancer_types, seq_length=dm.W, strands=2, chromosomes=23,
                                       hidden_size=128, layers=1, proj_size=0,
                                       recursion_limit=5,
                                       validation_hook_batch=next(iter(dm.val_dataloader())),  # TODO: update to all set
                                       test_hook_batch=next(iter(dm.test_dataloader())),       # TODO: update to all set
                                       run_id=f"ascat"
                                       )

    if True:
        trainer.fit(model, datamodule=dm)
        print(f"best checkpoint: {trainer.checkpoint_callback.best_model_path}")
    else:
        model = model.load_from_checkpoint(trainer.checkpoint_callback.dirpath + "/ascat.ckpt")

    # Test model
    trainer.test(model, test_dataloaders=dm.test_dataloader())


if __name__ == '__main__':

    # run_ascat_example()
    run_sinusoidal_example()

