//
//  UICollectionViewCell+InitialViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/12.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "InitialViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"

@interface InitialViewController ()<UICollectionViewDataSource,UICollectionViewDelegate>
{
    UICollectionView *mainCollectionView;
}

@end

@implementation InitialViewController

- (void)viewWillAppear:(BOOL)animated{
    [self.navigationController setNavigationBarHidden:YES animated:animated];
}

- (void)viewWillDisappear:(BOOL)animated{
    [self.navigationController setNavigationBarHidden:NO animated:animated];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.view addSubview: self.guideLabel];
    //inset distance to (top, left, bottom, right)
    UIEdgeInsets inset_title = UIEdgeInsetsMake(270, 100, 600, 100);
    [self.guideLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
    
    UICollectionViewFlowLayout *layout = [[UICollectionViewFlowLayout alloc] init];
    mainCollectionView = [[UICollectionView alloc] initWithFrame:self.view.bounds collectionViewLayout:layout];
    [self.view addSubview:mainCollectionView];
    
    //NSLog(@"%f, %f", mainCollectionView.frame.size.width, mainCollectionView.frame.size.height);
    
    
    mainCollectionView.bounds = CGRectMake(0, 0, self.view.frame.size.width * 0.5
                                           + 100, 20 * 4 + 100);
    
    mainCollectionView.backgroundColor = [UIColor clearColor];
    [mainCollectionView registerClass:[OperationCollectionViewCell class] forCellWithReuseIdentifier:@"cellId"];
    [mainCollectionView registerClass:[UICollectionReusableView class] forSupplementaryViewOfKind:UICollectionElementKindSectionHeader withReuseIdentifier:@"reusableView"];
       
       //4.设置代理
    mainCollectionView.delegate = self;
    mainCollectionView.dataSource = self;
    
    
    UIEdgeInsets inset_collection = UIEdgeInsetsMake(340, 100, 300, 100);
    
    [mainCollectionView mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_collection);
    }];
    
    NSLog(@"%ld", self.view.frame.size.width / 2 - 200 / 2);
}

- (NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView
{
    return 3;
}

- (NSInteger)collectionView:(nonnull UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section {
    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath
{

    OperationCollectionViewCell *cell = (OperationCollectionViewCell *)[collectionView dequeueReusableCellWithReuseIdentifier:@"cellId" forIndexPath:indexPath];
    
    //[cell.UnitButton setTitle:[NSString stringWithFormat:@"Unit %ld",(long)indexPath.section + 1] forState:0];
    
    OperationCollectionViewCell *cell_0 = (OperationCollectionViewCell *)[self->mainCollectionView cellForItemAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:0]];
                
    [cell_0.UnitButton setTitle:@"公司" forState:0];
    
    
    OperationCollectionViewCell *cell_1 = (OperationCollectionViewCell *)[self->mainCollectionView cellForItemAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:1]];
                
    [cell_1.UnitButton setTitle:@"单据" forState:0];
    
    
    OperationCollectionViewCell *cell_2 = (OperationCollectionViewCell *)[self->mainCollectionView cellForItemAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:2]];
                
    [cell_2.UnitButton setTitle:@"信用资产授权" forState:0];
    
    return cell;
}

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    AppDelegate *myDelegate = (AppDelegate*)[[UIApplication sharedApplication]delegate];
    
    //OperationCollectionViewCell *cell = (OperationCollectionViewCell *)[collectionView cellForItemAtIndexPath:indexPath];
    NSLog(@"%ld", indexPath.section);
    
    if(indexPath.section == 0) {
        SearchCompanyViewController* qc = [[SearchCompanyViewController alloc] init];
        qc.title = @"查询公司";
        [myDelegate.nc pushViewController:qc animated:YES];
    }
    
    
    if(indexPath.section == 1) {
        SearchReceiptViewController* qc = [[SearchReceiptViewController alloc] init];
        qc.title = @"查询单据";
        [myDelegate.nc pushViewController:qc animated:YES];
    }
    
    
    if(indexPath.section == 2) {
        SearchCreditAssetViewController* qc = [[SearchCreditAssetViewController alloc] init];
        qc.title = @"查询信用资产授权";
        [myDelegate.nc pushViewController:qc animated:YES];
    }
    
    /*
    qc.title = cell.UnitButton.titleLabel.text;
    NSLog(@"%@", qc.parentViewController.title);
    [myDelegate.nc pushViewController:qc animated:YES];
    NSLog(@"%ld", (long)indexPath.section + 1);
    */
    
}



- (CGFloat)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout minimumLineSpacingForSectionAtIndex:(NSInteger)section
{
    return 20;
}

-(UIEdgeInsets)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout insetForSectionAtIndex:(NSInteger)section
{
    return UIEdgeInsetsMake(10, 10, 10, 10);//分别为上、左、下、右
}

-(CGSize)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout sizeForItemAtIndexPath:(NSIndexPath*)indexPath{
    return CGSizeMake(200, 50);
}

- (UILabel *)guideLabel {
    if(_guideLabel == nil) {
        _guideLabel = [[UILabel alloc] init];
        [_guideLabel setText: @"请选择查询对象"];
        [_guideLabel setFont: [UIFont systemFontOfSize: 23]];
        [_guideLabel setTextColor: [UIColor blackColor]];
        [_guideLabel setTextAlignment:NSTextAlignmentCenter];
        //_guideLabel.backgroundColor = [UIColor blueColor];
    }
    return _guideLabel;
}

@end

